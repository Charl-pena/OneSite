import os
import sys
import json
# from bs4 import BeautifulSoup

def extract_number_from_filename(filename):
    try:
        return int(filename.split('_')[0])
    except ValueError:
        return float('inf')  # Si no es un número, colócalo al final

def procesar_archivo_html(ruta_html, carpeta_destino):
   # Lee el contenido del archivo HTML
   with open(ruta_html, 'r', encoding='utf-8') as file:
      html_content = file.read()
   
   # Construye el diccionario
   result_dict = {
      'HTMLContent': html_content,
   }
   # Convierte el diccionario a formato JSON
   json_result = json.dumps(result_dict, indent=2)

   # Construye la ruta completa al archivo JSON
      # Primero pasar a minusculas
   file_name_minuscula = os.path.basename(ruta_html).replace('.html', '.json')
   file_name_minuscula = file_name_minuscula[0].lower() + file_name_minuscula[1:]
   
   ruta_json = os.path.join(carpeta_destino, file_name_minuscula)

   # Escribe el resultado en un archivo JSON
   with open(ruta_json, 'w', encoding='utf-8') as json_file:
      json_file.write(json_result)

   print(f"JSON generado con éxito para {os.path.basename(ruta_html)}.")

def generar_json(carpeta_a_trabajar, carpeta_destino):
   logo = ""
   sectionName = ""
   nav_section = {}
   nav_sections = []
   flag_first_time = True

   for root, dirs, files in os.walk(carpeta_a_trabajar):
      for archivo in files:
         if ".html" in archivo:
            archivo_path = os.path.join(root, archivo)
            procesar_archivo_html(archivo_path, carpeta_destino)  
   
if __name__ == "__main__":
   if len(sys.argv) != 3:
      print("Uso: python script-pages.py <carpeta_a_trabajar> <carpeta_destino>")
      sys.exit(1)

   carpeta_destino    = sys.argv[2]
   carpeta_a_trabajar = sys.argv[1]

   if not os.path.isdir(carpeta_a_trabajar):
      print(f"La ruta proporcionada '{carpeta_a_trabajar}' no es una carpeta válida.")
      sys.exit(1)

   generar_json(carpeta_a_trabajar, carpeta_destino)
   

