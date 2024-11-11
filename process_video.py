import os
import asyncio
import psycopg2  # Asegúrate de que este módulo esté instalado
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import configparser
from selenium.webdriver.common.by import By
import psycopg2
import pyautogui
import logging
from db_connection_X_ import DatabaseConnection
class video_process:
    def __init__(self) :
        user_agent = UserAgent(platforms='pc')
        chrome_options = Options()

        self.download_dir = os.path.join(os.getcwd(), "videos_descargados")  # Carpeta de descargas
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)  # Crea la carpeta si no existe

        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self.download_dir,  # Carpeta de descarga
            "download.prompt_for_download": False,        # No pregunta antes de descargar
            "download.directory_upgrade": True,           # Reemplaza si ya existe
            "safebrowsing.enabled": True                  # Desactiva advertencias de seguridad
        })

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument(f'user-agent={user_agent.random}')
        #chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome( options= chrome_options)
        self.driver.maximize_window()
        self.page_link = 'https://x2twitter.com/es1'

        self.conexion = DatabaseConnection()
        self.conexion.crear_conexion()
    
    def generador_enlaces(self):
        try:
            with self.conexion.connection.cursor() as cursor:
                consulta = "SELECT url, id, publicacion_id FROM videos"  # Cambia la consulta para incluir id y publicacion_id
                cursor.execute(consulta)
                for resultado in cursor:
                    yield resultado  # Devuelve cada resultado (url, id, publicacion_id) de uno en uno
        except psycopg2.Error as e:
            logging.error(f"Error en la base de datos con la tabla videos: {e}")
        except Exception as e:
            logging.error(f"Algo está pasando al generar enlaces: {e}")
    async  def esperar_archivo(self,nombre_carpeta, tiempo_espera):
        tiempo_transcurrido = 0
        archivos_antes = set(os.listdir(nombre_carpeta))
        while tiempo_transcurrido < tiempo_espera:
            archivos_despues = set(os.listdir(nombre_carpeta))
            nuevos_archivos = archivos_despues - archivos_antes  # Detectar archivos nuevos
            for archivo in nuevos_archivos:
                if archivo.endswith('.mp4'):  # Verificar que sea un archivo de video
                    return archivo  # Devolver el nombre del archivo encontrado
            await asyncio.sleep(1)
            tiempo_transcurrido += 1
        return None 
    async def obtener_video(self):
        try:
            for url, video_id, publicacion_id in self.generador_enlaces():
                if url:
                    self.driver.get(self.page_link)
                    time.sleep(3)
                    input_enlace = self.driver.find_element(By.CSS_SELECTOR, "input[name='q']")
                    input_enlace.send_keys(url)
                    button_to_get = self.driver.find_element(By.CSS_SELECTOR, "button.btn-red")
                    time.sleep(3)
                    button_to_get.click()
                    time.sleep(3)
                    contador = 1
                    contenedor_videos = self.driver.find_element(By.CSS_SELECTOR, "div[id='data-result']")
                    videos=self.driver.find_elements(By.CSS_SELECTOR, "div.tw-video")
                    for video in videos:
                        WebDriverWait(video, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "p:nth-of-type(1) a[onclick='showAd()']"))
                        )
                        download_link = video.find_element(By.CSS_SELECTOR, "p:nth-of-type(1) a[onclick='showAd()']")
                        if "mp4" in download_link.text.lower():
                            download_url = download_link.get_attribute("href")
                            time.sleep(2)
                            self.driver.execute_script("window.open(arguments[0]);", download_url)
                            
                            # Espera la descarga del archivo y cambia su nombre si es necesario
                            archivo_descargado = await self.esperar_archivo("videos_descargados", 30)
                            if archivo_descargado:
                                self.cambiar_nombre(archivo_descargado, video_id, publicacion_id, contador)
                                contador += 1  # Incrementa el contador para el próximo video
                            else:
                                logging.error("No se encontró el archivo después del tiempo de espera.")
                            time.sleep(5)
                        else:
                            logging.info("El texto del enlace no contiene 'mp4', no se descargará el archivo.")
                else:
                    logging.error("No se pudo obtener el enlace.")
        except Exception as e:
            logging.error(f"Error al procesar los videos: {e}")
    def cambiar_nombre(self,archivo_descargado,video_id,publicacion_id,contador=1):
        download_dir = "videos_descargados"
        nuevo_nombre = f"{video_id}_{publicacion_id}_{contador}.mp4"
        nuevo_archivo = os.path.join(download_dir, nuevo_nombre)

        # Evitar conflictos de nombres
        while os.path.exists(nuevo_archivo):
            contador += 1
            nuevo_nombre = f"{video_id}_{publicacion_id}_{contador}.mp4"
            nuevo_archivo = os.path.join(download_dir, nuevo_nombre)
        
        os.rename(os.path.join(download_dir, archivo_descargado), nuevo_archivo)
        print(f"Video descargado y renombrado a: {nuevo_nombre}")
    def cerrar_conexion(self):
        try:
            self.conexion.connection.close()
            self.driver.quit()
            print("Conexión cerrada y navegador cerrado.")
        except Exception as e:
            logging.error(f"Error al cerrar la conexión o el navegador: {e}")
async def main():
    video_extractor = video_process()
    await video_extractor.obtener_video()
    video_extractor.cerrar_conexion()

if __name__ == "__main__":
 asyncio.run(main())