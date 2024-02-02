import os
import sys
import subprocess



def ejecutar_scripts():

    # Ejecutar el script script-docu
    ruta_script = "./script-docu.py"
    carpeta_a_trabajar = "null53-docu/"
    carpeta_a_crear =    "documentation/"
    subprocess.run(["python3", ruta_script, carpeta_a_trabajar, carpeta_a_crear])

    # Ejecutar el script script-navbar
    ruta_script = "./script-navbar.py"
    carpeta_a_trabajar = "null53-navbar/"
    archivo_json_a_crear = "navbar.json"
    subprocess.run(["python3", ruta_script, carpeta_a_trabajar, archivo_json_a_crear])
    

if __name__ == "__main__":
    ejecutar_scripts()
