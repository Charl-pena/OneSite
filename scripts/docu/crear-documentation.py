import os
import sys
import json
from bs4 import BeautifulSoup

def procesar_archivo_html(ruta_html):
    # Lee el contenido del archivo HTML
    with open(ruta_html, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Parsea el HTML usando BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

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

    # Construye el diccionario
    result_dict = {
        'Title': title,
        'Subtitle': subtitle,
    }
    
    return result_dict

def crear_json(json_necesario, carpeta_html_necesario, nombre_del_json):
	with open(json_necesario, 'r') as file:
		# Obtener el tamaño del archivo
		file_size = os.path.getsize(json_necesario)
		
		if file_size == 0:
			print(f"El JSON {json_path} está vacío.")
			return
		data = json.load(file)

	menu_items_without_submenus = []

	for section in data['MenuSections']:
		for menu_item in section['MenuItems']:
			menu_item_without_submenus = {k: v for k, v in menu_item.items() if k != 'SubMenus'}
			menu_items_without_submenus.append(menu_item_without_submenus)

	# Lista todos los archivos en el directorio
	archivos_en_carpeta = os.listdir(carpeta_html_necesario)
	# Filtra solo los archivos HTML
	archivos_html = [archivo for archivo in archivos_en_carpeta if archivo.endswith('.html')]
	if not archivos_html:
		print(f"No se encontraron archivos HTML en la carpeta {carpeta_html_necesario}.")
		result_data = {
			"Sections": menu_items_without_submenus
			}
	else:
		result_data_html = procesar_archivo_html(os.path.join(carpeta_html_necesario, archivos_html[0]))
		result_data = {
			**result_data_html,
			"Sections": menu_items_without_submenus
			}

	nombre_del_json = os.path.normpath(nombre_del_json)
	json_path = os.path.join(nombre_del_json, nombre_del_json) 
	with open(f"{json_path}.json", 'w') as output_file:
		json.dump(result_data, output_file, indent=2)

	print(f"Data has been saved to '{nombre_del_json}.json'")

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("Uso: python crear-documentation.py <json_necesario.json>, <carpeta_html_necesario>, <nombre_del_json")
		sys.exit(1)
  	
	carpeta_html_necesario  = sys.argv[2]
	json_necesario  = sys.argv[1]
	carpeta_a_crear = sys.argv[3]

	if not os.path.exists(json_necesario):
		print(f"La ruta proporcionada '{json_necesario}' no es un json válido.")
		sys.exit(1)

	if not os.path.isdir(carpeta_a_crear):
		print(f"La ruta proporcionada '{carpeta_a_crear}' no es una carpeta válida.")
		sys.exit(1)
	
	crear_json(json_necesario, carpeta_html_necesario, carpeta_a_crear)