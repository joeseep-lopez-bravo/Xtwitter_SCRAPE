
import os
import requests
import shutil
import psycopg2  # Asegúrate de que este módulo esté instalado
from db_connection_X_ import DatabaseConnection  # Importa tu clase de conexión a la base de datos
import configparser

# Crear una instancia de la conexión
conexion = DatabaseConnection()
conexion.crear_conexion()

def descargar_imagen(url, nombre_archivo):
    """Descarga una imagen desde la URL proporcionada y la guarda con el nombre de archivo indicado."""
    try:
        # Envía una solicitud GET a la URL
        respuesta = requests.get(url, stream=True)
        # Verifica si la solicitud fue exitosa (código 200)
        if respuesta.status_code == 200:
            # Abre un archivo en modo escritura binaria y guarda la imagen
            with open(nombre_archivo, 'wb') as archivo:
                shutil.copyfileobj(respuesta.raw, archivo)
            print(f"Imagen guardada como {nombre_archivo}")
        else:
            print(f"Error al descargar la imagen: {respuesta.status_code}")
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")

# Crear carpeta si no existe
carpeta_imagenes = 'imagenes_descargadas'
if not os.path.exists(carpeta_imagenes):
    os.makedirs(carpeta_imagenes)  # Crea la carpeta

# Leer el último ID procesado desde el archivo
ultimo_id_archivo = 'ultimo_id.txt'
ultimo_id = 0
if os.path.exists(ultimo_id_archivo):
    with open(ultimo_id_archivo, 'r') as file:
        ultimo_id = int(file.read().strip())
else:
    # Si no existe, crearlo y escribir el valor por defecto 0
    with open(ultimo_id_archivo, 'w') as file:
        file.write(str(ultimo_id))
    print(f"Archivo '{ultimo_id_archivo}' no encontrado. Creando archivo con valor 0.")
# Consulta para obtener los datos de la tabla imagenes a partir del último ID procesado
try:
    with conexion.connection.cursor() as cursor:
        # Modifica la consulta para obtener solo las imágenes nuevas
        consulta = "SELECT id, publicacion_id, url FROM imagen WHERE id > %s"
        cursor.execute(consulta, (ultimo_id,))
        resultados = cursor.fetchall()  # Obtener todos los resultados

        # Iterar sobre los resultados para descargar cada imagen
        for fila in resultados:
            id_imagen = fila[0]
            publicacion_id = fila[1]
            url_imagen = fila[2]

            # Generar nombre de archivo usando id y publicacion_id
            nombre_archivo = f"imagen_{id_imagen}_{publicacion_id}.jpg"
            
            # Crear la ruta completa del archivo en la carpeta creada
            ruta_archivo = os.path.join(carpeta_imagenes, nombre_archivo)
            
            # Llamar a la función para descargar la imagen
            descargar_imagen(url_imagen, ruta_archivo)

            # Actualizar el último ID procesado
            if id_imagen > ultimo_id:
                ultimo_id = id_imagen

    # Guardar el último ID procesado en el archivo
    with open(ultimo_id_archivo, 'w') as file:
        file.write(str(ultimo_id))

except Exception as e:
    print(f"Error al obtener los datos de la base de datos: {e}")
finally:
    # Cerrar la conexión después de usarla
    conexion.cerrar_conexion()
