import os
import sys
import json
from bs4 import BeautifulSoup

def extraer_logo(archivo):
   contenido = ""
   with open(archivo, 'r') as archivo:
      # Lee el contenido del archivo
      contenido = archivo.read()
   return contenido

def procesar_archivo_html(ruta_html):
   # Lee el contenido del archivo HTML
   with open(ruta_html, 'r', encoding='utf-8') as file:
      html_content = file.read()
   
   # Parsea el HTML usando BeautifulSoup
   soup = BeautifulSoup(html_content, 'html.parser')
   # Extrae el Icon, título y el subtítulo
   # Verificar si existe el elemento 'icon'
   if hasattr(soup, 'icon') and soup.icon:
      icon = soup.icon.text.strip()
   else:
      icon = None  # Otra acción que desees realizar en caso de que no exista 'icon'
   # Verificar si existe el elemento 'title'
   if hasattr(soup, 'title') and soup.title:
      title = soup.title.text.strip()
      title = title.capitalize()
   else:
      title = None  # Otra acción que desees realizar en caso de que no exista 'title'
   # Verificar si existe el elemento 'subtitle'
   if hasattr(soup, 'subtitle') and soup.subtitle:
      subtitle = soup.subtitle.text.strip()
   else:
      subtitle = None
       
   href = os.path.basename(ruta_html).lower().replace(".html", "")
   # Construye el diccionario
   result_dict = {
       'Href': href + '/',
       'Title': title,
       'Subtitle': subtitle,
       'IconClass': icon,
   }

   return result_dict

def crear_navjson(nav_sections, logo, file_name):
   result_json = {
      "Logo": logo,
      "NavSections": nav_sections
   }
   # Convertir a formato JSON
   result_json_str = json.dumps(result_json, indent=2)

   # Escribe el resultado en un archivo JSON
   with open(file_name, 'w', encoding='utf-8') as json_file:
      json_file.write(result_json_str)

   print(f"JSON generado con éxito para {file_name}.")


def generar_json(carpeta_a_trabajar, archivo_json_a_crear):
   logo = ""
   sectionName = ""
   nav_section = {}
   nav_sections = []
   flag_first_time = True

   for root, dirs, files in os.walk(carpeta_a_trabajar):
      if root == carpeta_a_trabajar:
         archivo = files[0]
         if ".txt" in archivo:
            logo = extraer_logo(os.path.join(root, archivo))
      else:
         # print(root)
         for archivo in files:
            # print(f"huevos {sectionName} JAJAJA {os.path.basename(root)}")
            if sectionName != os.path.basename(root):
               sectionName = os.path.basename(root) 
               
               if flag_first_time is True:
                  flag_first_time = False
               else:
                  nav_sections.append(nav_section.copy())
               nav_section["NameSection"] = sectionName
               nav_section["MenuItems"]   = []

            nav_section["MenuItems"].append(procesar_archivo_html(os.path.join(root, archivo)))

   nav_sections.append(nav_section)
   crear_navjson(nav_sections, logo, archivo_json_a_crear)      
   

if __name__ == "__main__":
   if len(sys.argv) != 3:
      print("Uso: python script-navbar.py <carpeta_a_trabajar> <archivo_json_a_crear>")
      sys.exit(1)

   carpeta_a_trabajar = sys.argv[1]
   archivo_json_a_crear=sys.argv[2]
   if not os.path.isdir(carpeta_a_trabajar):
      print(f"La ruta proporcionada '{carpeta_a_trabajar}' no es una carpeta válida.")
      sys.exit(1)

   generar_json(carpeta_a_trabajar, archivo_json_a_crear)
   

