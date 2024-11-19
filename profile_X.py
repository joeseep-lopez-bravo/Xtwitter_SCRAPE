from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,WebDriverException,TimeoutException
import pyautogui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import uuid
import time
import configparser
import random
from selenium.webdriver.common.by import By
import psycopg2
import logging
from db_connection_X_ import DatabaseConnection
from sys import exit
class Scraper_Perfil_X:
    def __init__(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")  # Activar modo headless
        #chrome_options.add_argument("--disable-gpu")  # Opcional: mejora en algunos entornos
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--disable-notifications")
        #chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome( options= chrome_options)
        self.driver.maximize_window()
        self.config = configparser.ConfigParser()
        self.config.read('credentials.conf')
        self.credentials = self._get_credentials()
        #self.email = self.config.get('DEFAULT','emailkey')
        #self.username = self.config.get('DEFAULT','usernamekey')
        #self.password = self.config.get('DEFAULT','passwordkey')
        self.perfil_links = [
            "https://x.com/realDonaldTrump",
           # 'https://x.com/WH40kbestof',
           # 'https://x.com/EmergenciasEc',
        ]
        self.conexion = DatabaseConnection()
        self.conexion.crear_conexion()  
    def _get_credentials(self):
        credentials = []
        # Filtrar las claves que contienen pares coincidentes de username y password
        for key in self.config['DEFAULT']:
            if key.startswith('usernamekey'):
                num = key.replace('usernamekey', '')
                email = self.config.get('DEFAULT', f'emailkey{num}')
                username = self.config.get('DEFAULT', f'usernamekey{num}')
                password = self.config.get('DEFAULT', f'passwordkey{num}')
                credentials.append((email,username, password))
        return credentials
    def login(self,attempt = 0):
        max_attempts = len(self.credentials)
        while attempt < max_attempts and self.credentials:
                email,username, password = random.choice(self.credentials)
                logging.info(f"Iniciando sesión con el usuario: {username} (Intento {attempt + 1})")
                try:    
                    time.sleep(1)
                    target_url = 'https://x.com/i/flow/login'
                    self.driver.get(target_url) 
                    time.sleep(2)
                    
                    email_text_in_input = WebDriverWait(self.driver, 15).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "label div div[dir='ltr'] span"))
                    )
                    email_text_in_input=email_text_in_input.text
                    if "correo electrónico" in email_text_in_input.lower():
                         email_input = WebDriverWait(self.driver, 15).until(
                         EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='text']"))
                    )
                         
                         #email_input = self.driver.find_element("css selector","input[name='text']")
                         email_input.send_keys(email)
                         btton_to_pssword=self.driver.find_element("css selector","button.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-ywje51.r-184id4b.r-13qz1uu.r-2yi16.r-1qi8awa.r-3pj75a.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l")
                         btton_to_pssword.click()
                    time.sleep(1)
                    try:
                        username_text_input = self.driver.find_element("css selector","input[name='text']")
                        username_text_input.send_keys(username)
                        btton_to_username=self.driver.find_element("css selector","button[data-testid='ocfEnterTextNextButton']")
                        btton_to_username.click()
                        time.sleep(1)
                    except:
                        #logging.info("No borrar el catch vacio , no hay nada pero si lo borras no funcionara bien ")
                        pass
                    
                    password_text_in_input = WebDriverWait(self.driver, 15).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "div:nth-of-type(1) >label div div[dir='ltr'] span"))
                    )
                    password_text_in_input = password_text_in_input.text

                    if "contraseña" in password_text_in_input.lower():
                        password_input = WebDriverWait(self.driver, 15).until(
                            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
                        )
                        password_input.send_keys(password)

                    login = self.driver.find_element("css selector", "button[data-testid='LoginForm_Login_Button']").click()
                    time.sleep(3)  
                    if "login_attempt" in self.driver.current_url or "checkpoint" in self.driver.current_url:
                        raise ValueError("Inicio de sesión fallido, el perfil puede estar bloqueado o las credenciales son incorrectas.")
                    else:
                        logging.info(f"Sesión iniciada con éxito con el usuario: {username}")
                        return self.driver.page_source 
                except Exception as e:
                    logging.info(f"Error en el intento {attempt + 1}: {e}")
                
                    self.credentials.remove((email, username, password))  # Eliminar credenciales fallidas
                    self.driver.get("https://x.com/i/flow/login")  # Volver a la página de inicio de sesión
                    time.sleep(2)
                    
        # Llamar recursivamente para un nuevo intento
        return self.login(attempt + 1)
    def configurar_logger(self):
        # Configuración básica del logger
        logging.basicConfig(filename='Logs_Scraper_twitter.log',  # Archivo donde se guardarán los logs
                            level=logging.INFO,     # Nivel de registro, en este caso errores
                            format='%(asctime)s - %(levelname)s - %(message)s',  # Formato del log
                            datefmt='%Y-%m-%d %H:%M:%S')  # Formato de la fecha y hora  
    def scroll_hasta_el_final(self,driver):
        scroll_distance = random.randint(1200, 1500)  # Randomize scroll distance
        current_scroll_position = driver.execute_script("return window.pageYOffset;")
        target_scroll_position = current_scroll_position + scroll_distance
        driver.execute_script(f"window.scrollTo(0, {target_scroll_position});")
        time.sleep(random.uniform(0, 1.5))  # Randomize delay to mimic human behavior

    def scroll_hasta_el_final_post(self,driver):
        scroll_distance = random.randint(500, 580)  # Randomize scroll distance
        #logging.info("La distnacia movida en post fue o es :" , scroll_distance)
        current_scroll_position = driver.execute_script("return window.pageYOffset;")
        target_scroll_position = current_scroll_position + scroll_distance
        driver.execute_script(f"window.scrollTo(0, {target_scroll_position});")
        time.sleep(random.uniform(0, 1))  # Randomize delay to mimic human behavior    
    def obtener_posts(self,driver):
        try:
            feed_div = driver.find_element(By.CSS_SELECTOR, "section[role='region']:nth-of-type(1)")
            return feed_div.find_elements(By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']")
        except NoSuchElementException as e:
            logging.error(f"Error: Could not locate the 'feed_div' or 'cellInnerDiv' elements. : {e}")
        except Exception as e:
            logging.error(f"Unexpected error in obtener_posts: {e}" )
        return []
    def obtener_videos(self,elemento_base):
        # Locate the element you want to right-click on
        try:
            url_post_video = elemento_base.find_element(By.CSS_SELECTOR, "div.css-175oi2r.r-18u37iz.r-1q142lx a").get_attribute('href')
            url_to_downloand= url_post_video
            #logging.info("video enlace : ", url_to_downloand)
            return url_to_downloand
        except:
            logging.info("Ocurrio un error al obtener el video o este post no contiene videos")
            return None
            pass
    def obtener_imagenes(self,driver,elemento_base):
        selector_multi_image = [
        "div.css-175oi2r.r-1pi2tsx.r-13qz1uu.r-18u37iz",
        "div.css-175oi2r.r-1pi2tsx.r-13qz1uu.r-eqz5dr"
        ]
    
        div_content_multiimages = None
        
        # Intentar encontrar el contenedor usando cada selector
        for selector in selector_multi_image:
            try:
                div_content_multiimages = elemento_base.find_element(By.CSS_SELECTOR, selector)
                WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.css-175oi2r.r-16y2uox.r-1pi2tsx.r-13qz1uu")
                )                                 
            )
                break  # Si lo encuentra, sale del bucle
            except NoSuchElementException:
                logging.info("No contiene imagenes")

        if div_content_multiimages:
            # Encuentra los contenedores de imágenes dentro del contenedor encontrado
            div_content_images = div_content_multiimages.find_elements(By.CSS_SELECTOR, "div.css-175oi2r.r-16y2uox.r-1pi2tsx.r-13qz1uu")
            time.sleep(1)
            for div_content_image in div_content_images:
                try:
                    # Obtén el enlace de la imagen
                    src_link = div_content_image.find_element(By.CSS_SELECTOR, "img[alt='Image']").get_attribute("src")
                    logging.info(f"El url de una de las imagenes:, {src_link}")
                    yield src_link 
                except NoSuchElementException:
                    # En caso de que no encuentre la imagen en este contenedor
                    logging.info("No contiene imagenes")
                    continue
        else:
            logging.info("No contiene imagenes")        
    def obtener_comentarios(self,driver,publicacion_id):
            try:
                #obtener por hora publicada
                event=True
                comentarios_vistos = set()
                time.sleep(1)
                # Obtén la nueva URL actual
                url_actual = driver.current_url
                contador_repeticiones = 0 
                contador_comentarios_repetidos = 0
                longitud_anterior = -1 
                while event: 
                # Llama al siguiente método
                    try:
                        coments= self.obtener_posts(driver)
                        self.scroll_hasta_el_final(driver)
                    except Exception as e:
                        logging.error(f"error al llamar funciones en comentarios {e}")
                        logging.info(f"Nueva URL: {url_actual}")
                    longitud_actual = len(coments)
                    if longitud_actual == longitud_anterior:
                        contador_repeticiones += 1  # Incrementa el contador si es igual
                    else:
                        contador_repeticiones = 0  # Reinicia el contador si no es igual
                    # Actualiza la longitud anterior con la longitud actual
                    longitud_anterior = longitud_actual
                    # Si la longitud se ha repetido 20 veces, cambia event a False
                    if contador_repeticiones >= 8:
                        logging.info("La longitud de comentarios se ha repetido 8 veces. Terminando la extracción de comentarios del post actual.")
                        event = False  # Termina el bucle
                    try:
                        i=0
                        for comment in coments:
                            try:
                                texto = comment.text
                                i+=1
                                if texto not in comentarios_vistos:  # Verifica si el texto ya fue procesado
                                    comentarios_vistos.add(texto) 
                                    logging.info(f"Estamos en el iterador de comentarios :  {i}")
                                    
                                    try:
                                        div_global_info_post = comment.find_element(By.CSS_SELECTOR, "div.css-175oi2r.r-1iusvr4.r-16y2uox.r-1777fci.r-kzbkwu")
                                        div_user_poster = div_global_info_post.find_element(By.CSS_SELECTOR, "div.css-175oi2r.r-zl2h9q span.css-1jxf684.r-dnmrzs.r-1udh08x.r-3s2u2q.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3 span")
                                        usuario= div_user_poster.text;
                                        logging.info(f"El usuario comentador : {usuario}")
                                        #time.sleep(1)
                                        try:
                                            div_contenido = div_global_info_post.find_element(By.CSS_SELECTOR, "div.css-175oi2r div[data-testid='tweetText']")
                                            descripcion_comentario = div_contenido.text
                                            logging.info(f"El contenido o descripcion comentario : {descripcion_comentario}")
                                            #time.sleep(1)
                                        except:
                                            logging.info("Este comentario no contiene descripcion")
                                        try:
                                            
                                            with self.conexion.connection.cursor() as cursor:
                                                    consulta_verificacion = "SELECT id FROM comentario WHERE usuario = %s AND descripcion_comentario = %s AND  publicacion_id= %s"
                                                    cursor.execute(consulta_verificacion, (usuario, descripcion_comentario,publicacion_id ))
                                                    resultado = cursor.fetchone()
                                                    if(resultado == None):
                                                        consulta = "INSERT INTO comentario (publicacion_id, usuario,descripcion_comentario) VALUES (%s, %s,%s) RETURNING id"
                                                        cursor.execute(consulta, (publicacion_id,usuario, descripcion_comentario))
                                                        self.conexion.connection.commit()
                                                        comentario_id = cursor.fetchone()[0]
                                                        logging.info(f"Comentario insertada con éxito.")
                                                    else:
                                                         logging.info("comentario ya doble y repetido,no ingestado a la db")
                                                         contador_comentarios_repetidos += 1   
                                                         if(contador_comentarios_repetidos >= 6):
                                                            logging.info("Se reptitio mas de 6 comentarios , obviamos los demas comentarios")
                                                            event=False 
                                                                      
                                        except psycopg2.Error as e:
                                                    logging.error(f"Error en la base de datos con la comentario  {e}" )
                                        except Exception as e:
                                                    logging.error(f"algo esta mal con la insercion del comentario")
                                        try:
                                            #time.sleep(1)
                                            div_img= div_global_info_post.find_element(By.CSS_SELECTOR,"div >div.css-175oi2r.r-1mlwlqe.r-1udh08x.r-417010.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af > img[alt='Image']")
                                            src_link = div_img.get_attribute("src")
                                            logging.info(f"El url de la imagen del comentario: {src_link}")
                                            try:
                                                with self.conexion.connection.cursor() as cursor:
                                                    consulta_verificacion = "SELECT id FROM imagen WHERE url = %s AND publicacion_id =%s"
                                                    cursor.execute(consulta_verificacion, (src_link,publicacion_id))
                                                    resultado = cursor.fetchone()
                                                    logging.info(f"El id repetido es: {resultado}")
                                                    if resultado==None:
                                                        consulta = "INSERT INTO imagen (url,publicacion_id,comentario_id) VALUES (%s, %s,%s)"
                                                        cursor.execute(consulta, (src_link,publicacion_id,comentario_id ))
                                                        self.conexion.connection.commit() # Asegúrate de confirmar la transacción
                                                        logging.info(f"Imagen  de comentario insertada con éxito")
                                                    else :
                                                         logging.info("NO SE INSERTO IMAGEN COMO ELEMENTO REPETIDO")    
                                        
                                            except psycopg2.Error as e:
                                                        logging.error(f"Error en la base de datos Imagenes con la publicación  con id : {publicacion_id} en el grupo :    : {e}")
                                            except Exception as e:
                                                        logging.error(f"Algo está pasando con esto Imagenes: {e}")
                                        except:
                                            logging.error("Ese post no contiene una Imagen")
                                    
                                        
                                        enlaceimagenes=self.obtener_imagenes(driver,div_global_info_post)
                                        for enlace in enlaceimagenes:
                                            #logging.info('url de imagen:', enlace)
                                            try:
                                                with self.conexion.connection.cursor() as cursor:
                                                        consulta_verificacion = "SELECT id FROM imagen WHERE url = %s "
                                                        cursor.execute(consulta_verificacion, (enlace,))
                                                        resultado = cursor.fetchone()
                                                        logging.info(f"El id repetido en imagenes es: {resultado}")
                                                        if resultado==None:
                                                            consulta = "INSERT INTO imagen (url,publicacion_id,comentario_id) VALUES (%s, %s,%s)"
                                                            cursor.execute(consulta, (enlace,publicacion_id,comentario_id ))
                                                            self.conexion.connection.commit() # Asegúrate de confirmar la transacción
                                                            logging.info(f"Imagen insertada con éxito")
                                                        else :
                                                            logging.info("NO SE INSERTO IMAGEN ELEMENTO REPETIDO")  
                                            except psycopg2.Error as e:
                                                        logging.error(f"Error en la base de datos Imagenes con la publicación  con id : {publicacion_id} en el grupo :    : {e}")
                                            except Exception as e:
                                                        logging.error(f"Algo está pasando con esto Imagenes: {e}")
                                        try:
                                                selector_video= div_global_info_post.find_element(By.CSS_SELECTOR, "video")
                                                if selector_video:
                                                    url_actual=self.obtener_videos(div_global_info_post)
                                                    try:
                                                            with self.conexion.connection.cursor() as cursor:
                                                                consulta_verificacion = "SELECT id FROM videos WHERE url = %s AND publicacion_id =%s"
                                                                cursor.execute(consulta_verificacion, (url_actual,publicacion_id))
                                                                resultado = cursor.fetchone()
                                                                
                                                                if resultado is None and url_actual is not None:
                                                                        consulta = "INSERT INTO videos (url, publicacion_id,comentario_id) VALUES (%s, %s,%s) "
                                                                        cursor.execute(consulta, (url_actual,publicacion_id,comentario_id))
                                                                        self.conexion.connection.commit() 
                                                                        logging.info("Comentario video insertado con éxitos")
                                                                else:
                                                                    logging.info(f"El id repetido en videos es: {resultado}")
                                                                    logging.info("NO SE INSERTO VIDEO ELEMENTO REPETIDO")        
                                                    except psycopg2.Error as e:
                                                                    logging.error(f"Error en la base de datos con la tabla videos: {e}")
                                                    except Exception as e:
                                                                    logging.error(f"Algo está pasando conn el video insertado: {e}")
                                                else:
                                                    logging.info("algo salio mal en video ,el post no contiene un video")    
                                                pass
                                        except Exception as e:
                                                #logging.error("Ocurrio un error al obtener descripcions del video", e) 
                                                pass                            
                                    except:
                                        logging.error("Error en obtner el div global en comentarios,es divisor y no publicacion")
                                        pass
                            except Exception as e:
                                #logging.error("Error dentro del bucle for",e)   
                                pass     
                    except Exception as e:
                            logging.error(f"Error dentro del bucle for {e}")    
                #time.sleep(1)
                #logging.error("Se hizo lick al boton para retroceder")
            except Exception as e:
                logging.error(f"Ocurrio error en procesar comentarios {e}")
                pass

    def obtener_retweets(self,driver,elemento_base,publicacion_id,type_post):
            try:
                logging.info(f"El post es de tipo: {type_post}")
                if type_post.lower() != "respuesta":
                    clickeable_post_coment = WebDriverWait(elemento_base, 15).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.css-175oi2r.r-18u37iz.r-1q142lx a"))
                        )
                    #clickeable_post_coment = elemento_base.find_element(By.CSS_SELECTOR, "div.css-175oi2r.r-18u37iz.r-1q142lx a")
                    ActionChains(driver).move_to_element(clickeable_post_coment).click().perform()
                    time.sleep(1)
                    logging.info("hice click para ver dentro del post")
                    try:
                        button_menu_tweets = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='retweet']"))
                        )
                        # Desplazarse al elemento para garantizar que sea clickeable
                        ActionChains(driver).move_to_element(button_menu_tweets).perform()
                        # Intentar hacer clic
                        button_menu_tweets.click()
                    except Exception as e:
                        logging.error(f"Error en el primer tweet open menu:  {e}")
                    time.sleep(1)
                    try:
                        button_go_to_menu_retweets = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[role='menuitem']:nth-of-type(2)"))
                        )

                        ActionChains(driver).move_to_element(button_go_to_menu_retweets).perform()

                        button_go_to_menu_retweets.click()
                    except Exception as e:
                        logging.error(f"Error en el 2do tweet selecto quotes:  {e}")
                    # Pausa para asegurarse de que la página cargue
                    #time.sleep(1)
                    time.sleep(1)
                    # Esperar y hacer clic en el botón para ver los retweets
                    try:
                        button_to_see_retweets = WebDriverWait(driver, 15).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='ScrollSnap-List'] > div:nth-of-type(2) a[role='tab']"))
                        )
                        button_to_see_retweets.click()
                    except Exception as e:
                        logging.error(f"Error en el 3er tweet select:  {e}")

                    
                    
                    event=True
                    time.sleep(1)
                    # Obtén la nueva URL actual
                    url_actual = driver.current_url
                    contador_repeticiones = 0 
                    contador_retweet_repetidos = 0
                    longitud_anterior = -1 
                    retweets_vistos = set()
                    logging.info(f"Estamos dentro de en la publicacion {publicacion_id}")
                    while event:     
                        try:
                            self.scroll_hasta_el_final(driver)
                            tweets= self.obtener_posts(driver)
                        except Exception as e:
                            logging.error(f"error al llamar funciones en cretweets {e}")
                            logging.info(f"Nueva URL: {url_actual}")
                        longitud_actual = len(tweets)
                        if longitud_actual == longitud_anterior:
                            contador_repeticiones += 1  # Incrementa el contador si es igual
                        else:
                            contador_repeticiones = 0  # Reinicia el contador si no es igual
                        # Actualiza la longitud anterior con la longitud actual
                        longitud_anterior = longitud_actual
                        # Si la longitud se ha repetido 20 veces, cambia event a False
                        if contador_repeticiones >= 5:
                            logging.info("La longitud de retweets se ha repetido 5 veces. Terminando la extracción de comentarios del post actual.")
                            event = False  # Termina el bucle      
                        
                        try:
                            for tweet in tweets:
                                    try:
                                        div_username = tweet.find_element(By.CSS_SELECTOR, "div>div[dir='ltr'] > span > span:nth-of-type(1)")
                                        username_retweet = div_username.text
                                        username_retweet = username_retweet.strip().lower()
                                        logging.info(f"El usuario que dio retweet : {username_retweet}")
                                        
                                        if username_retweet not in retweets_vistos: 
                                            retweets_vistos.add(username_retweet)
                                            
                                            #print("Usuario que paso del filtro if ",username_retweet)
                                            #print(f"Longitud del conjunto retweets_vistos: {len(retweets_vistos)}")
                                            #print(f"Valores en retweets_vistos: {retweets_vistos}")
                                            try:
                                                
                                                with self.conexion.connection.cursor() as cursor:
                                                        consulta_verificacion = "SELECT id FROM retweet  WHERE publicacion_id = %s AND usuario = %s "
                                                        cursor.execute(consulta_verificacion, (publicacion_id,username_retweet ))
                                                        resultado = cursor.fetchone()
                                                        
                                                        if resultado== None:
                                                            consulta = "INSERT INTO retweet (publicacion_id, usuario) VALUES (%s,%s) "
                                                            cursor.execute(consulta, (publicacion_id,username_retweet))
                                                            self.conexion.connection.commit()
                                                            logging.info(f"retweet insertada con éxito.")  
                                                            # que pasa despues de insertar con extio
                                                        else: 
                                                            '''consulta_total = "SELECT count(*) FROM retweet WHERE publicacion_id = %s "
                                                            cursor.execute(consulta_total, (publicacion_id,))
                                                            resultado_total = cursor.fetchone()[0]
                                                            limite_repetidos = resultado_total // 2'''
                                                            logging.info("retweet ya doble y repetido,no ingestado a la db")
                                                            contador_retweet_repetidos += 1   
                                                            if(contador_retweet_repetidos > 5):
                                                                logging.info("Se reptitio mas de 5 retweet , obviamos los demas retweets")
                                                                event=False
                                                                break
                                            except psycopg2.Error as e:
                                                        logging.error(f"Error en la base de datos con la retweet  {e}")
                                            except Exception as e:
                                                        logging.error(f"algo esta mal con la insercion del retweet")
                                        else:
                                             logging.info("user retweet ya en el conjutno")
                                             continue
                                        
                                    except:
                                        logging.error(f"Error dentro del bucle for retwettv{e}")           
                        except Exception as e:
                            #logging.error(f"sucede algo dentro tweets{e}")
                            pass 
                    try:
                        exit_post_coment = WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Back']"))
                    )
                        exit_post_coment.click()
                        logging.info("Realicé click para salir")
                    except Exception as e:
                        logging.info("No se salio del 1er back" ,e)
                    try:    
                        exit_post_coment = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Back']"))
                    )
                        exit_post_coment.click()   
                    except Exception as e:
                        logging.info("No se salio del 2do back")
                    try:
                        num_comment=driver.find_element(By.CSS_SELECTOR,"div.css-175oi2r.r-18u37iz.r-1h0z5md.r-13awgt0:nth-of-type(1) button div[dir='ltr'] div.css-175oi2r.r-xoduu5.r-1udh08x:nth-of-type(2) span span")
                        num_comment_text = num_comment.text
                        num_comment_value = int(num_comment_text) if num_comment_text.isdigit() else 0

                        logging.info(f"Número de comentarios: {num_comment_value}")
                        
                        # Si el número de comentarios es 1 o más, ejecuta el método obtener_comentarios
                        if num_comment_value >= 1:
                            self.obtener_comentarios(driver,publicacion_id)
                            # logging.info("Despues de obtner comentarios", event)
                            pass
                        else:
                            logging.info("No hay comentarios para procesar.")
                    except Exception as e:
                        logging.error(f"Ocurrió un error al querer obtener comentarios: {e}")           
                    try:
                        exit_post_coment = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Back']"))
                        )
                        exit_post_coment.click() 
                        logging.info("le dicick al tercer boton") 
                    except:
                        logging.info("No se salio del 3er back")  
                else:
                     logging.error("No se procedio a obtener tweets de publicacion tipo respuesta")
                     pass
                #obtener por hora publicada
                
            except Exception as e:    
                logging.error(f"Aqui hay errores en obtener_retweets {e}")
                pass
    def extraer_datos(self,driver):
        try:
            elementos_vistos = set()
            event =True  
            contador_repeticiones = 0  # Contador para verificar repeticiones
            longitud_anterior = -1  # Inicializamos en -1 para que sea diferente de la primera longitud
            try:
                while event:  # Bucle infinito hasta que se detenga manualmente
                    try:
                        self.scroll_hasta_el_final_post(driver)
                        divs = self.obtener_posts(driver)  # Obtiene los elementos actuales
                        i =0
                        longitud_actual = len(divs)
                        logging.info(f'Cantidad total de divs: {longitud_actual}')
                        if longitud_actual == longitud_anterior:
                            contador_repeticiones += 1  # Incrementa el contador si es igual
                        else:
                            contador_repeticiones = 0  # Reinicia el contador si no es igual
                        # Actualiza la longitud anterior con la longitud actual
                        longitud_anterior = longitud_actual
                        # Si la longitud se ha repetido 20 veces, cambia event a False
                        if contador_repeticiones >= 10:
                            logging.info("La longitud de divs se ha repetido 10 veces. Terminando la extracción.")
                            event = False  # Termina el bucle
                        try:
                            for div in divs:
                                #el problema es que cuando encuentra publiaciones que responden a otros se bugea
                                #logging.info("Este es el texto" ,texto)
                                i+=1
                                logging.info(f"Estamos en el iterador :  {i}")
                                try:
                                    div_global_info_post = div.find_element(By.CSS_SELECTOR, "div.css-175oi2r.r-1iusvr4.r-16y2uox.r-1777fci.r-kzbkwu")
                                    div_user_poster = div_global_info_post.find_element(By.CSS_SELECTOR, "div.css-175oi2r.r-zl2h9q span.css-1jxf684.r-dnmrzs.r-1udh08x.r-3s2u2q.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3 span")
                                    post_usuario = div_user_poster.text
                                    logging.info(f"El usuario : {post_usuario}")
                                except: 
                                    #logging.info("Este post no contiene usuario")   
                                    pass
                                try:
                                    div_contenido = div_global_info_post.find_element(By.CSS_SELECTOR, "div.css-175oi2r div[data-testid='tweetText']")
                                    descripcion_post= div_contenido.text
                                    logging.info(f"Descripcion post : {descripcion_post}")
                                    #time.sleep(1)
                                except:
                                    descripcion_post=" "
                                    logging.info("Este post no contiene descripcion")
                                time.sleep(1)    
                                try:
                                        num_likes=div_global_info_post.find_element(By.CSS_SELECTOR,"div.css-175oi2r.r-18u37iz.r-1h0z5md.r-13awgt0:nth-of-type(3) button div[dir='ltr'] div.css-175oi2r.r-xoduu5.r-1udh08x:nth-of-type(2) span span")
                                        num_likes_text = num_likes.text                 
                                except Exception as e:    
                                        num_likes_text = 0    
                                        #logging.error(f"Problema en extraer los likes en tweets  {e}") 
                                        pass
                                texto = post_usuario + descripcion_post
                                #logging.info("El valor de :",texto)
                                try:
                                    post_replier = div_global_info_post.find_element(
                                        By.CSS_SELECTOR, "div.css-175oi2r.r-4qtqp9.r-zl2h9q > div[dir='ltr']"
                                    )
                                    post_replier_text = post_replier.text
                                    if "Replying to" in post_replier_text:
                                        type_post = "respuesta"
                                        logging.info("Es post tipo respuesta")
                                    else:
                                        type_post = "otro_tipo"
                                        logging.info("Es algo nuevo y diferente que 'Replying to'")
                                except Exception as e:  # Captura el caso donde el elemento no existe
                                        type_post = "post_normal"
                                        #logging.error("No se encontró el elemento para determinar el tipo de publicación.",e)
                                        pass
                                
                                if texto not in elementos_vistos:  # Verifica si el texto ya fue procesado
                                    elementos_vistos.add(texto)  
                                
                                    try:
                                        with self.conexion.connection.cursor() as cursor:
                                            consulta_verificacion = "SELECT id FROM publicacion WHERE descripcion = %s AND usuario = %s "
                                            cursor.execute(consulta_verificacion, (descripcion_post, post_usuario))
                                            resultado = cursor.fetchone()
                                            # Si no existe, insertar
                                            if resultado is None:
                                                consulta_insercion = "INSERT INTO publicacion (descripcion, usuario,likes) VALUES (%s, %s,%s) RETURNING id"
                                                cursor.execute(consulta_insercion, (descripcion_post, post_usuario, num_likes_text ))
                                                publicacion_id = cursor.fetchone()[0]
                                                self.conexion.connection.commit()
                                                logging.info(f"Publicación insertada con éxito. ID de la publicación: {publicacion_id}")
                                            else:
                                                
                                                publicacion_id = resultado[0]
                                                    # Solo actualizar si el número de likes ha cambiado
                                                '''try: 
                                                    consulta_actualizacion = "UPDATE publicacion SET likes = %s WHERE id = %s"
                                                    cursor.execute(consulta_actualizacion, (num_likes_text, publicacion_id))
                                                    self.conexion.connection.commit()
                                                    logging.info(f"Publicación duplicada detectada. ID existente: {publicacion_id}")
                                                except Exception as e:
                                                        logging.info(f"Ocurrio un error en el desarrollo de actualizacion de likes y obtencion del id {e}")'''
                                    except psycopg2.Error as e:
                                                logging.error(f"Error en la base de datos con la publicación  con id : {publicacion_id}  {e} ")
                                    except Exception as e:
                                                logging.error(f"algo esta mal con la insercion de la publicacion con id : {publicacion_id} ")
                                                                
                                    try:
                                        #ime.sleep(1)
                                        div_img= div_global_info_post.find_element(By.CSS_SELECTOR,"div >div.css-175oi2r.r-1mlwlqe.r-1udh08x.r-417010.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af > img[alt='Image']")
                                        src_link = div_img.get_attribute("src")
                                        logging.info(f"El url de la imagen: {src_link}")
                                        try:
                                            with self.conexion.connection.cursor() as cursor:
                                                consulta_verificacion = "SELECT id FROM imagen WHERE url = %s "
                                                cursor.execute(consulta_verificacion, (src_link,))
                                                resultado = cursor.fetchone()

                                                if(resultado == None):
                                                    consulta = "INSERT INTO imagen (url,publicacion_id) VALUES (%s, %s)"
                                                    cursor.execute(consulta, (src_link,publicacion_id ))
                                                    self.conexion.connection.commit() # Asegúrate de confirmar la transacción
                                                    logging.info(f"Imagen insertada con éxito")
                                                else:   
                                                    logging.info(f"Imagen duplicada detectada. ID existente pertenece a publicacion con id : {publicacion_id}")
                                        except psycopg2.Error as e:
                                                    logging.error(f"Error en la base de datos Imagenes con la publicación  con id : {publicacion_id} en el grupo :    : {e}")
                                        except Exception as e:
                                                    logging.error(f"Algo está pasando con esto Imagenes: {e}")
                                    except:
                                        logging.error("Ese post no contiene una Imagen")

                                    enlaceimagenes=self.obtener_imagenes(driver,div_global_info_post)
                                    for enlace in enlaceimagenes:
                                        #logging.info('url de imagen:', enlace)
                                        try:
                                            with self.conexion.connection.cursor() as cursor:
                                                        consulta_verificacion = "SELECT id FROM imagen WHERE url = %s "
                                                        cursor.execute(consulta_verificacion, (src_link,))
                                                        resultado = cursor.fetchone()
                                                        if (resultado == None):
                                                            consulta = "INSERT INTO imagen (url,publicacion_id) VALUES (%s, %s)"
                                                            cursor.execute(consulta, (enlace,publicacion_id ))
                                                            self.conexion.connection.commit() # Asegúrate de confirmar la transacción
                                                            logging.info(f"Imagen insertada con éxito")
                                                        else: 
                                                            logging.info(f"Imagen duplicada detectada. ID existente pertenece a publicacion con id : {publicacion_id}")
                                    
                                        except psycopg2.Error as e:
                                                    logging.error(f"Error en la base de datos Imagenes con la publicación  con id : {publicacion_id} en el grupo :    : {e}")
                                        except Exception as e:
                                                    logging.error(f"Algo está pasando con esto Imagenes: {e}")       
                                    try:
                                        selector_video= div_global_info_post.find_element(By.CSS_SELECTOR, "video")
                                        
                                        if selector_video:
                                            url_actual=self.obtener_videos(div_global_info_post)
                                            try:
                                                    with self.conexion.connection.cursor() as cursor:
                                                        consulta_verificacion = "SELECT id FROM videos WHERE url = %s "
                                                        cursor.execute(consulta_verificacion, (url_actual,))
                                                        resultado = cursor.fetchone()
                                                        logging.info(f"El id repetido en video es: {resultado}")
                                                        if (resultado==None):
                                                            consulta = "INSERT INTO videos (url, publicacion_id) VALUES (%s, %s) "
                                                            cursor.execute(consulta, (url_actual,publicacion_id))
                                                            self.conexion.connection.commit() 
                                                            logging.info(f"Video insertado con éxitos  {url_actual}")
                                                        else:
                                                                logging.info("No se inserto video repetido")    
                                            except psycopg2.Error as e:
                                                            logging.error(f"Error en la base de datos con la tabla videos: {e}")
                                            except Exception as e:
                                                            logging.error(f"Algo está pasando conn el video insertado: {e}")
                                        else:
                                            #logging.error("algo salio mal en video")    
                                            pass
                                    except Exception as e:
                                        #logging.error("Ocurrio un error al obtener descripcions del video", e) 
                                        pass
                                    
                                    try:
                                        self.obtener_retweets(driver,div_global_info_post,publicacion_id,type_post)
                                        
                                    except Exception as e:    
                                        logging.error(f"Algo paso dentro de llamar a retwees {e}")
                                    #yield publicacion_id 
                                else:
                                     logging.error(f"El texto ya ha sido procesado. Saltando al siguiente div: {publicacion_id}")
                                     continue        
                        except Exception as e:
                            #logging.error("Error dentro de extraer datos de for",e) 
                            pass                       
                    except Exception as e:
                        #logging.error("Error dentro del while pero antes del for",e)
                        pass
            except Exception as e:
                logging.error(f"Error dentro de extraer datos de while ene xtraccion genral de datos {e}")   
                pass    
        except Exception as e:
            logging.error(f"Error dentro de extraer datos in funcion {e}")                       
    def procesar_perfiles(self):
        try:
            self.configurar_logger()
            logging.info("Iniciando procesamiento de perfiles...")
            self.login()
            self.config.read('topics.conf')
            try:
                if 'DEFAULT' in self.config and 'topic' in self.config['DEFAULT']:
                    topics_str = self.config.get('DEFAULT', 'topic')
                    self.topics = [topic.strip() for topic in topics_str.strip("[]").replace("'", "").split(",")]
                else:
                    logging.info("La opción 'topic' no se encontró en la sección 'DEFAULT'")
                logging.info(f"Temas a buscar: {self.topics}")
            except Exception as e :
                 logging.error(f"Problemas con  topics  {e}" )
            # Iterar sobre cada tema para realizar la búsqueda
            for topic in self.topics:
                logging.info(f"Realizando búsqueda de: {topic}")
                time.sleep(1)
                # Hacer clic en el ícono de búsqueda
                div_search = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Search and explore']"))
                )
                div_search.click()

                search_topic = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search query']"))
                )
                search_topic.clear()
                search_topic.send_keys(topic)  # Asignar el tema actual al campo de búsqueda
                search_topic.send_keys(Keys.RETURN)
                time.sleep(1)
                logging.info(f"Extrayendo resultados para el tema {topic}...")
                action = ActionChains(self.driver)
                action.key_down(Keys.CONTROL)
                # Simular Ctrl + Scroll hacia atrás (Zoom Out)
                pyautogui.keyDown('ctrl')  # Mantén presionada la tecla Ctrl
                for _ in range(3):  # Ajusta la cantidad de zoom out según sea necesario
                    pyautogui.scroll(-500)  # Desplazar hacia atrás para hacer zoom out
                    time.sleep(1)  # Pausa breve para que el navegador procese el zoom
                pyautogui.keyUp('ctrl') 
                try:
                    for dato in self.extraer_datos(self.driver):
                        logging.info('siguiente post:')
                except Exception as e:
                    logging.error(f"Error dentro de extraer datos fuera {e}")
                #grupos_procesados += 1 
                #logging.info(f"Grupos procesados: {grupos_procesados}/{total_grupos}")

        except Exception as e:
            logging.error(f"Error al procesar grupos: {e}")

        finally:
            # Asegurarse de que el navegador se cierra al terminar el procesamiento de todos los grupos
            if self.driver:
                self.driver.quit()
    def cerrar_conexion(self):
        self.driver.quit()    
        self.conexion.cerrar_conexion()
        pass
def main():    
    scraper_perfil = Scraper_Perfil_X() 
    scraper_perfil.procesar_perfiles()
    scraper_perfil.cerrar_conexion()
    pass 
if __name__ == "__main__":
    main() 
    

