import configparser
import psycopg2
from psycopg2 import OperationalError

class DatabaseConnection:
    def __init__(self, config_file='db_credentials.ini'):
        self.config_file = config_file
        self.connection = None

    def crear_conexion(self):
        """Crea una conexión a la base de datos usando las credenciales del archivo de configuración."""
        config = configparser.ConfigParser()
        try:
            config.read(self.config_file)
            if 'DB' not in config.sections():
                raise KeyError("Sección 'DB' no encontrada en el archivo de configuración.")
            print("Secciones disponibles:", config.sections())  # Imprime las secciones para depurar
            print("Contenido de la sección DB:", dict(config.items('DB')))  # Imprime los valores de la sección DB
        except Exception as e:
            print(f"Error al leer el archivo de configuración: {e}")
            return

        try:
            db_config = {
                'dbname': config.get('DB', 'dbname'),
                'user': config.get('DB', 'user'),
                'password': config.get('DB', 'password'),
                'host': config.get('DB', 'host'),
                'port': config.get('DB', 'port', fallback='5432')
            }
            self.connection = psycopg2.connect(**db_config)
            print("Conexión exitosa a la base de datos.")
        except configparser.NoOptionError as e:
            print(f"Error: Falta una opción en la configuración: {e}")
        except UnicodeDecodeError as e:
            print("Error de codificación:", e)
        except psycopg2.Error as e:
            print("Error en la conexión a la base de datos:", e)
        except OperationalError as e:
            print(f"Error al conectar a la base de datos: {e}")

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos."""
        if self.connection:
            self.connection.close()
            print("Conexión cerrada")

   
# Uso de la clase
if __name__ == "__main__":
    db = DatabaseConnection()
    db.crear_conexion()
    print("Hey aquí te saludo desde la conexión")
    # Aquí puedes realizar operaciones con la base de datos
    db.cerrar_conexion()
