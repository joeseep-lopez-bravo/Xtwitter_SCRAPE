from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,WebDriverException
import pyautogui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--disable-notifications")
        #chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome( options= chrome_options)
        self.driver.maximize_window()
        self.config = configparser.ConfigParser()
        self.config.read('credentials.conf')
        self.email = self.config.get('DEFAULT','emailkey')
        self.username = self.config.get('DEFAULT','usernamekey')
        self.password = self.config.get('DEFAULT','passwordkey')
        self.perfil_links = [
            "https://x.com/realDonaldTrump",
           # 'https://x.com/WH40kbestof',
           # 'https://x.com/EmergenciasEc',
        ]
        self.conexion = DatabaseConnection()
        self.conexion.crear_conexion()  
    def login(self):
        time.sleep(3)
        target_url = 'https://x.com/i/flow/login'
        self.driver.get(target_url) 
        time.sleep(4)
        email_input = self.driver.find_element("css selector","input[name='text']")
        email_input.send_keys(self.email)
        btton_to_pssword=self.driver.find_element("css selector","button.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-ywje51.r-184id4b.r-13qz1uu.r-2yi16.r-1qi8awa.r-3pj75a.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l")
        btton_to_pssword.click()
        time.sleep(4)
        try:
            username_input = self.driver.find_element("css selector","input[name='text']")
            username_input.send_keys(self.username)
            btton_to_username=self.driver.find_element("css selector","button[data-testid='ocfEnterTextNextButton']")
            btton_to_username.click()
            time.sleep(4)
        except:
            pass
        password_input = self.driver.find_element("css selector", "input[name='password']")
        password_input.send_keys(self.password)
        login = self.driver.find_element("css selector", "button[data-testid='LoginForm_Login_Button']").click()
        time.sleep(6)  
    def scroll_hasta_el_final(self,driver):
        scroll_distance = random.randint(1300, 1800)  # Randomize scroll distance
        current_scroll_position = driver.execute_script("return window.pageYOffset;")
        target_scroll_position = current_scroll_position + scroll_distance
        driver.execute_script(f"window.scrollTo(0, {target_scroll_position});")
        time.sleep(random.uniform(0, 1.5))  # Randomize delay to mimic human behavior
    def obtener_posts(self,driver):
        try:
            feed_div = driver.find_element(By.CSS_SELECTOR, "section[role='region']:nth-of-type(1)")
            return feed_div.find_elements(By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']")
        except NoSuchElementException as e:
            print("Error: Could not locate the 'feed_div' or 'cellInnerDiv' elements.", e)
        except Exception as e:
            print("Unexpected error in obtener_posts:", e)
        return []
    def obtener_videos(self,elemento_base):

        # Locate the element you want to right-click on
        try:
            url_post_video = elemento_base.find_element(By.CSS_SELECTOR, "div.css-175oi2r.r-18u37iz.r-1q142lx a").get_attribute('href')
            url_to_downloand= url_post_video
            #print("video enlace : ", url_to_downloand)
            yield url_to_downloand
        except:
            print("Ocurrio un error al obtener el video")
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
                print("No contiene imagenes")

        if div_content_multiimages:
            # Encuentra los contenedores de imágenes dentro del contenedor encontrado
            div_content_images = div_content_multiimages.find_elements(By.CSS_SELECTOR, "div.css-175oi2r.r-16y2uox.r-1pi2tsx.r-13qz1uu")
            time.sleep(5)
            for div_content_image in div_content_images:
                try:
                    # Obtén el enlace de la imagen
                    src_link = div_content_image.find_element(By.CSS_SELECTOR, "img[alt='Image']").get_attribute("src")
                    print("El url de una de las imagenes:", src_link)
                    yield src_link 
                except NoSuchElementException:
                    # En caso de que no encuentre la imagen en este contenedor
                    print("Algo pasa con las imagenes")
                    continue
        else:
            print("No contiene imagenes")        
    def obtener_comentarios(self,driver,elemento_base,publicacion_id):
        try:
            #obtener por hora publicada
             try:
                clickeable_post_coment = elemento_base.find_element(By.CSS_SELECTOR, "div.css-175oi2r.r-18u37iz.r-1q142lx a")
                ActionChains(driver).move_to_element(clickeable_post_coment).click().perform()
             except:
                print("Erroe n click de enlace a comentarios")
             event=True
             comentarios_vistos = set()
             time.sleep(1)
            # Obtén la nueva URL actual
             url_actual = driver.current_url
             contador_repeticiones = 0 
             longitud_anterior = -1 
             while event: 
            # Llama al siguiente método
                try:
                    self.scroll_hasta_el_final(driver)
                    coments= self.obtener_posts(driver)
                except Exception as e:
                    print("error al llamar funciones", e)
                    print("Nueva URL:", url_actual)
                longitud_actual = len(coments)
                if longitud_actual == longitud_anterior:
                    contador_repeticiones += 1  # Incrementa el contador si es igual
                else:
                    contador_repeticiones = 0  # Reinicia el contador si no es igual
                # Actualiza la longitud anterior con la longitud actual
                longitud_anterior = longitud_actual
                # Si la longitud se ha repetido 20 veces, cambia event a False
                if contador_repeticiones >= 8:
                    print("La longitud de comentarios se ha repetido 8 veces. Terminando la extracción de comentarios del post actual.")
                    event = False  # Termina el bucle
                try:
                    i=0
                    for comment in coments:
                        try:
                            texto = comment.text
                            i+=1
                            if texto not in comentarios_vistos:  # Verifica si el texto ya fue procesado
                                comentarios_vistos.add(texto) 
                                print("Estamos en el iterador de comentarios : ", i)
                                try:
                                    div_global_info_post = comment.find_element(By.CSS_SELECTOR, "div.css-175oi2r.r-1iusvr4.r-16y2uox.r-1777fci.r-kzbkwu")
                                    div_user_poster = div_global_info_post.find_element(By.CSS_SELECTOR, "div.css-175oi2r.r-zl2h9q span.css-1jxf684.r-dnmrzs.r-1udh08x.r-3s2u2q.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3 span")
                                    usuario= div_user_poster.text;
                                    print("El usuario comentador :", div_user_poster.text)
                                    time.sleep(1)
                                    try:
                                        div_contenido = div_global_info_post.find_element(By.CSS_SELECTOR, "div.css-175oi2r div[data-testid='tweetText']")
                                        print("El contenido o descripcion comentario :", div_contenido.text)
                                        descripcion_comentario = div_contenido.text
                                        time.sleep(1)
                                    except:
                                        print("Este comentario no contiene descripcion")
                                    try:
                                        with self.conexion.connection.cursor() as cursor:
                                                consulta = "INSERT INTO comentario (publicacion_id, usuario,descripcion_comentario) VALUES (%s, %s,%s) RETURNING id"
                                                cursor.execute(consulta, (publicacion_id,usuario, descripcion_comentario))
                                                self.conexion.connection.commit()
                                                comentario_id = cursor.fetchone()[0]
                                                print(f"Comentario insertada con éxito.")         
                                    except psycopg2.Error as e:
                                                logging.error(f"Error en la base de datos con la comentario  " ,e)
                                    except Exception as e:
                                                logging.error(f"algo esta mal con la insercion del comentario")
                                    try:
                                        time.sleep(1)
                                        div_img= div_global_info_post.find_element(By.CSS_SELECTOR,"div >div.css-175oi2r.r-1mlwlqe.r-1udh08x.r-417010.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af > img[alt='Image']")
                                        src_link = div_img.get_attribute("src")
                                        print("El url de la imagen del comentario:", src_link)
                                    except:
                                        print("Ese post no contiene una Imagen")
                                    enlaceimagenes=self.obtener_imagenes(driver,div_global_info_post)
                                    for enlace in enlaceimagenes:
                                        #print('url de imagen:', enlace)
                                        try:
                                            with self.conexion.connection.cursor() as cursor:
                                                    consulta = "INSERT INTO imagen (url,publicacion_id,comentario_id) VALUES (%s, %s,%s)"
                                                    cursor.execute(consulta, (enlace,publicacion_id,comentario_id ))
                                                    self.conexion.connection.commit() # Asegúrate de confirmar la transacción
                                                    print(f"Imagen insertada con éxito")
                                    
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
                                                            consulta = "INSERT INTO videos (url, publicacion_id,comentario_id) VALUES (%s, %s,%s) "
                                                            cursor.execute(consulta, (url_actual,publicacion_id,comentario_id))
                                                            self.conexion.connection.commit() 
                                                            print("Comentario insertado con éxitos")
                                                except psycopg2.Error as e:
                                                                logging.error(f"Error en la base de datos con la tabla videos: {e}")
                                                except Exception as e:
                                                                logging.error(f"Algo está pasando conn el video insertado: {e}")
                                            else:
                                                print("algo salio mal en video")    
                                            pass
                                    except Exception as e:
                                            #print("Ocurrio un error al obtener descripcions del video", e) 
                                            pass                            
                                except:
                                    print("Error en obtner el div global")
                                    pass
                        except Exception as e:
                            #print("Error dentro del bucle for",e)   
                            pass     
                except Exception as e:
                        print("Error dentro del bucle for",e)    
             time.sleep(1)
             exit_post_coment = driver.find_element(By.CSS_SELECTOR,"button[aria-label='Back']")
             exit_post_coment.click()
             #print("Se hizo lick al boton para retroceder")
        except Exception as e:
            print("Ocurrio error en procesar comentarios" , e)
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
                        self.scroll_hasta_el_final(driver)
                        divs = self.obtener_posts(driver)  # Obtiene los elementos actuales
                        i =0
                        time.sleep(2)
                        longitud_actual = len(divs)
                        print('Cantidad total de divs: ', longitud_actual)
                        if longitud_actual == longitud_anterior:
                            contador_repeticiones += 1  # Incrementa el contador si es igual
                        else:
                            contador_repeticiones = 0  # Reinicia el contador si no es igual
                        # Actualiza la longitud anterior con la longitud actual
                        longitud_anterior = longitud_actual
                        # Si la longitud se ha repetido 20 veces, cambia event a False
                        if contador_repeticiones >= 13:
                            print("La longitud de divs se ha repetido 13 veces. Terminando la extracción.")
                            event = False  # Termina el bucle
                        try:
                            for div in divs:
                                texto = div.text
                                i+=1
                                if texto not in elementos_vistos:  # Verifica si el texto ya fue procesado
                                    elementos_vistos.add(texto) 
                                    print("Estamos en el iterador : ", i)
                                    try:
                                        div_global_info_post = div.find_element(By.CSS_SELECTOR, "div.css-175oi2r.r-1iusvr4.r-16y2uox.r-1777fci.r-kzbkwu")
                                        div_user_poster = div_global_info_post.find_element(By.CSS_SELECTOR, "div.css-175oi2r.r-zl2h9q span.css-1jxf684.r-dnmrzs.r-1udh08x.r-3s2u2q.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3 span")
                                        print("El usuario :", div_user_poster.text)
                                        post_usuario = div_user_poster.text
                                        time.sleep(1)
                                        try:
                                            div_contenido = div_global_info_post.find_element(By.CSS_SELECTOR, "div.css-175oi2r div[data-testid='tweetText']")
                                            descripcion_post= div_contenido.text
                                            print("El contenido o descripcion :", div_contenido.text)
                                            time.sleep(1)
                                        except:
                                            print("Este post no contiene descripcion")
                                        try:
                                            with self.conexion.connection.cursor() as cursor:
                                                    consulta = "INSERT INTO publicacion (descripcion, usuario) VALUES (%s, %s) RETURNING id"
                                                    cursor.execute(consulta, (descripcion_post, post_usuario))
                                                    self.conexion.connection.commit() # Asegúrate de confirmar la transacción
                                                    publicacion_id = cursor.fetchone()[0]
                                                    self.conexion.connection.commit()  # Asegúrate de confirmar la transacción
                                                    print(f"Publicación insertada con éxito. ID de la publicación: {publicacion_id}")         
                                        except psycopg2.Error as e:
                                                    logging.error(f"Error en la base de datos con la publicación  con id : {publicacion_id}  ", e)
                                        except Exception as e:
                                                    logging.error(f"algo esta mal con la insercion de la publicacion con id : {publicacion_id} ")
                                                
                                        try:
                                            time.sleep(1)
                                            div_img= div_global_info_post.find_element(By.CSS_SELECTOR,"div >div.css-175oi2r.r-1mlwlqe.r-1udh08x.r-417010.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af > img[alt='Image']")
                                            src_link = div_img.get_attribute("src")
                                            print("El url de la imagen:", src_link)
                                            try:
                                                with self.conexion.connection.cursor() as cursor:
                                                    consulta = "INSERT INTO imagen (url,publicacion_id) VALUES (%s, %s)"
                                                    cursor.execute(consulta, (src_link,publicacion_id ))
                                                    self.conexion.connection.commit() # Asegúrate de confirmar la transacción
                                                    print(f"Imagen insertada con éxito")
                                        
                                            except psycopg2.Error as e:
                                                        logging.error(f"Error en la base de datos Imagenes con la publicación  con id : {publicacion_id} en el grupo :    : {e}")
                                            except Exception as e:
                                                        logging.error(f"Algo está pasando con esto Imagenes: {e}")

                                        except:
                                            print("Ese post no contiene una Imagen")
                                        enlaceimagenes=self.obtener_imagenes(driver,div_global_info_post)
                                        for enlace in enlaceimagenes:
                                            #print('url de imagen:', enlace)
                                            try:
                                                with self.conexion.connection.cursor() as cursor:
                                                        consulta = "INSERT INTO imagen (url,publicacion_id) VALUES (%s, %s)"
                                                        cursor.execute(consulta, (enlace,publicacion_id ))
                                                        self.conexion.connection.commit() # Asegúrate de confirmar la transacción
                                                        print(f"Imagen insertada con éxito")
                                        
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
                                                            consulta = "INSERT INTO videos (url, publicacion_id) VALUES (%s, %s) "
                                                            cursor.execute(consulta, (url_actual,publicacion_id))
                                                            self.conexion.connection.commit() 
                                                            print("Video insertado con éxitos" , url_actual)
                                                except psycopg2.Error as e:
                                                                logging.error(f"Error en la base de datos con la tabla videos: {e}")
                                                except Exception as e:
                                                                logging.error(f"Algo está pasando conn el video insertado: {e}")
                                            else:
                                                print("algo salio mal en video")    
                                            pass
                                        except Exception as e:
                                            #print("Ocurrio un error al obtener descripcions del video", e) 
                                            pass
                                        try:
                                            num_comment=div_global_info_post.find_element(By.CSS_SELECTOR,"div.css-175oi2r.r-18u37iz.r-1h0z5md.r-13awgt0:nth-of-type(1) button div[dir='ltr'] div.css-175oi2r.r-xoduu5.r-1udh08x:nth-of-type(2) span span")
                                            num_comment_text = num_comment.text
                                            num_comment_value = int(num_comment_text) if num_comment_text.isdigit() else 0

                                            print("Número de comentarios:", num_comment_value)
                                            
                                            # Si el número de comentarios es 1 o más, ejecuta el método obtener_comentarios
                                            if num_comment_value >= 1:
                                                self.obtener_comentarios(driver, div_global_info_post,publicacion_id)
                                                print("Despues de obtner comentarios", event)
                                                
                                            else:
                                                print("No hay comentarios para procesar.")
                                        except Exception as e:
                                            print("Ocurrió un error:", e)
                                           
                                    except Exception as e:
                                        print("error con e" ,e)
                                        pass   
                        except Exception as e:
                            #print("Error dentro de extraer datos de for",e) 
                            pass                       
                    except Exception as e:
                        print("Error dentro del while pero antes del for",e)
            except Exception as e:
                print("Error dentro de extraer datos de while",e)   
        except Exception as e:
            print("Error dentro de extraer datos  dentro",e)                       
    def procesar_perfiles(self):
        try:
            self.login()

            self.config.read('topics.conf')
            if 'DEFAULT' in self.config and 'topic' in self.config['DEFAULT']:
                topics_str = self.config.get('DEFAULT', 'topic')
                self.topics = [topic.strip() for topic in topics_str.strip("[]").replace("'", "").split(",")]
            else:
                print("La opción 'topic' no se encontró en la sección 'DEFAULT'")
            print("Temas a buscar:", self.topics)
            
            # Iterar sobre cada tema para realizar la búsqueda
            for topic in self.topics:
                print(f"Realizando búsqueda de: {topic}")
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
                print(f"Extrayendo resultados para el tema '{topic}'...")
                action = ActionChains(self.driver)
                action.key_down(Keys.CONTROL)
                # Simular Ctrl + Scroll hacia atrás (Zoom Out)
                pyautogui.keyDown('ctrl')  # Mantén presionada la tecla Ctrl
                for _ in range(3):  # Ajusta la cantidad de zoom out según sea necesario
                    pyautogui.scroll(-240)  # Desplazar hacia atrás para hacer zoom out
                    time.sleep(1)  # Pausa breve para que el navegador procese el zoom
                pyautogui.keyUp('ctrl') 
                try:
                    for dato in self.extraer_datos(self.driver):
                        print('next :')
                except Exception as e:
                    print("Error dentro de extraer datos fuera", e)
                #grupos_procesados += 1 
                #print(f"Grupos procesados: {grupos_procesados}/{total_grupos}")

        except Exception as e:
            logging.error(f"Error al procesar grupos: {e}")

        finally:
            # Asegurarse de que el navegador se cierra al terminar el procesamiento de todos los grupos
            if self.driver:
                self.driver.quit()
    def cerrar_conexion(self):
        pass
def main():    
    scraper_perfil = Scraper_Perfil_X() 
    scraper_perfil.procesar_perfiles()
    pass 
if __name__ == "__main__":
    main() 
    

