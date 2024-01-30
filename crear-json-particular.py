import sys
from bs4 import BeautifulSoup
import json
import os

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

    # Busca el elemento subtitle y su siguiente hermano
    subtitle_element = soup.find('subtitle')
    html_content = ''
    if subtitle_element:
        next_sibling = subtitle_element.find_next_sibling()
        while next_sibling:
            html_content += str(next_sibling)
            next_sibling = next_sibling.find_next_sibling()

    # Construye el diccionario
    result_dict = {
        'Title': title,
        'Subtitle': subtitle,
        'Icon': icon,
        'HTMLContent': html_content,
    }

    # Convierte el diccionario a formato JSON
    json_result = json.dumps(result_dict, indent=2)

    file_name_minuscula = os.path.basename(ruta_html).replace('.html', '.json')
    file_name_minuscula = file_name_minuscula[0].lower() + file_name_minuscula[1:]
    # Construye la ruta completa al archivo JSON
    # 
    ruta_json = os.path.join(os.path.dirname(ruta_html), file_name_minuscula)

    # Escribe el resultado en un archivo JSON
    with open(ruta_json, 'w', encoding='utf-8') as json_file:
        json_file.write(json_result)

    print(f"JSON generado con éxito para {os.path.basename(ruta_html)}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python crear-json-particular.py <ruta_carpeta>")
        sys.exit(1)

    carpeta_html = sys.argv[1]

    if not os.path.isdir(carpeta_html):
        print(f"La ruta proporcionada '{carpeta_html}' no es una carpeta válida.")
        sys.exit(1)

    archivos_html = [f for f in os.listdir(carpeta_html) if f.endswith('.html')]

    if archivos_html:
        for archivo_html in archivos_html:
            ruta_html = os.path.join(carpeta_html, archivo_html)
            procesar_archivo_html(ruta_html)
    else:
        print("No se encontraron archivos html.")