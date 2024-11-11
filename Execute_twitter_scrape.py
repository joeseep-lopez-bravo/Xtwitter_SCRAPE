import subprocess

# Variables para almacenar los subprocesos en ejecución
processes = []
def ejecutar_script1():
    print("Ejecutando script páginas...")
    process = subprocess.Popen(["python", "profile_X.py"])
    processes.append(process)
    process.wait()  # Espera a que el primer script termine antes de continuar

def ejecutar_script2():
    print("Ejecutando script obtener imágenes...")
    process = subprocess.Popen(["python", "process_image.py"])
    processes.append(process)
    process.wait()  # Espera a que el segundo script termine antes de continuar

def ejecutar_script3():
    print("Ejecutando script obtener videos...")
    process = subprocess.Popen(["python", "process_video.py"])
    processes.append(process)
    process.wait()  # Espera a que el tercer script termine antes de continuar

# Función para ejecutar todos los scripts en secuencia
def ejecutar_todos_los_scripts():
    ejecutar_script1()  # Ejecuta y espera a que termine el script 1
    ejecutar_script3()  # Ejecuta y espera a que termine el script 3
    ejecutar_script2()  # Ejecuta y espera a que termine el script 2

# Función para cancelar todos los scripts en ejecución
def cancelar_todos_los_scripts():
    for process in processes:
        if process.poll() is None:  # Verifica si el proceso sigue en ejecución
            print("Cancelando script...")
            process.terminate()
    processes.clear()  # Limpia la lista de procesos

# Ejecutar todos los scripts en secuencia
if __name__ == "__main__":
    try:
        ejecutar_todos_los_scripts()
        print("Todos los scripts se han ejecutado.")
    except KeyboardInterrupt:
        print("Cancelando todos los scripts...")
        cancelar_todos_los_scripts()