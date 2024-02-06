import os
import sys
import shutil
import subprocess



def ejecutar_scripts():

    # Ejecutar el script script-docu
    ruta_script = "./script-docu.py"
    carpeta_a_trabajar = "null53-docu/"
    carpeta_a_crear =    "documentation/"
    subprocess.run(["python3", ruta_script, carpeta_a_trabajar, carpeta_a_crear])

    # Proceso: Crear carpeta index
    carpeta_index = "./index"
    # Verificar si la carpeta existe
    if os.path.exists(carpeta_index):
        # Eliminar la carpeta si existe
        shutil.rmtree(carpeta_index)
        print(f'Carpeta "{carpeta_index}" eliminada.')

    # Crear la carpeta
    os.makedirs(carpeta_index)

    # Ejecutar el script script-navbar
    ruta_script = "./script-navbar.py"
    carpeta_a_trabajar = "null53-navbar/"
    archivo_json_a_crear = os.path.join(carpeta_index, "navbar.json")
    subprocess.run(["python3", ruta_script, carpeta_a_trabajar, archivo_json_a_crear])
    
    # Ejecutar el script script-pages
    ruta_script = "./script-pages.py"
    carpeta_a_trabajar = "null53-pages/"
    subprocess.run(["python3", ruta_script, carpeta_a_trabajar, carpeta_index])
    
if __name__ == "__main__":
    ejecutar_scripts()
