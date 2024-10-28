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
        self.password = self.config.get('DEFAULT','passwordkey')
        self.perfil_links = [
            'https://x.com/EmergenciasEc',
        ]
        
    def login(self):
        time.sleep(3)
        target_url = 'https://x.com/i/flow/login'
        self.driver.get(target_url) 
        time.sleep(5)
        email_input = self.driver.find_element("css selector","input[name='text']")
        email_input.send_keys(self.email)
        btton_to_pssword=self.driver.find_element("css selector","button.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-ywje51.r-184id4b.r-13qz1uu.r-2yi16.r-1qi8awa.r-3pj75a.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l")
        btton_to_pssword.click()
        time.sleep(5)
        password_input = self.driver.find_element("css selector", "input[name='password']")
        password_input.send_keys(self.password)
        login = self.driver.find_element("css selector", "button[data-testid='LoginForm_Login_Button']").click()
        time.sleep(6)
    def perfil_generador(self,perfil_links):
        for perfil_link in perfil_links:
            yield perfil_link      
    def scroll_hasta_el_final(self,driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
    def obtener_posts(self,driver):
        try:
            feed_div = driver.find_element("css selector", "section[role='region']")
            WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']")
                )                                 
            )
            return feed_div.find_elements(By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']")
        except Exception as e:                                         
            #logging.error(f"Error al obtener los divs hijos en el grupo {perfil_link}")
            print("Error en iterador de post")
            return []
    def perfil_generador(self, perfiles_links):
        for pagina_link in perfiles_links:
            yield pagina_link
    def obtener_imagenes(self,driver,elemento_base):
        
        
        pass

    def extraer_datos(self,driver,group_name,perfil_link):
        elementos_vistos = set()
        event =True  
        contador_repeticiones = 0  # Contador para verificar repeticiones
        longitud_anterior = -1  # Inicializamos en -1 para que sea diferente de la primera longitud
        while event:  # Bucle infinito hasta que se detenga manualmente
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
            for div in divs:
                texto = div.text
                i+=1
                if texto not in elementos_vistos:  # Verifica si el texto ya fue procesado
                    elementos_vistos.add(texto) 
                    try:
                        div_global_info_post = div.find_element(By.CSS_SELECTOR, "div.css-175oi2r.r-1iusvr4.r-16y2uox.r-1777fci.r-kzbkwu")
                        div_user_poster = div_global_info_post.find_element(By.CSS_SELECTOR, "div.css-175oi2r.r-zl2h9q span.css-1jxf684.r-dnmrzs.r-1udh08x.r-3s2u2q.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3 span")
                        print("El usuario :", div_user_poster.text)
                        
                        try:
                            div_contenido = div_global_info_post.find_element(By.CSS_SELECTOR, "div.css-175oi2r div[data-testid='tweetText']")
                            print("El contenido o descripcion :", div_contenido.text)
                        except:
                            print("Este post no contiene descripcion")
                        try:
                            div_img= div_global_info_post.find_element(By.CSS_SELECTOR,"div >div.css-175oi2r.r-1mlwlqe.r-1udh08x.r-417010.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af > img[alt='Image']")
                            src_link = div_img.get_attribute("src")
                            print("El url de la imagen:", src_link)
                        except:
                            print("Ese post no contiene una Imagen")
                    except:
                        pass
    def procesar_perfiles(self):
        try:
            self.login()
            generador_grupos = self.perfil_generador(self.perfil_links)
            total_grupos = len(self.perfil_links)  # Total de grupos a procesar
            print("hay  perfiles " ,total_grupos)
            grupos_procesados = 0  # Contador de grupos procesados   
            for perfil_link in generador_grupos:
                self.driver.get(perfil_link)  # Cargar el siguiente grupo
                time.sleep(3)
                #self.driver.execute_script("document.body.style.zoom='50%'")
                print(f"Extrayendo información de {perfil_link}...")
                action = ActionChains(self.driver)
                action.key_down(Keys.CONTROL)
                # Simular Ctrl + Scroll hacia atrás (Zoom Out)
                pyautogui.keyDown('ctrl')  # Mantén presionada la tecla Ctrl
                for _ in range(3):  # Ajusta la cantidad de zoom out según sea necesario
                    pyautogui.scroll(-150)  # Desplazar hacia atrás para hacer zoom out
                    time.sleep(1)  # Pausa breve para que el navegador procese el zoom
                pyautogui.keyUp('ctrl') 
                div_group_name = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.css-175oi2r.r-xoduu5.r-1awozwy.r-18u37iz.r-dnmrzs >span >span.css-1jxf684.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3"))
                )
                group_name = div_group_name.text
                for dato in self.extraer_datos(self.driver,group_name,perfil_link):
                    print('next :')

                grupos_procesados += 1 
                print(f"Grupos procesados: {grupos_procesados}/{total_grupos}")
            self.conexion.cerrar_conexion()

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
    

