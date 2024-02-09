import os
import json
import sys
from bs4 import BeautifulSoup

def extract_number_from_filename(filename):
    try:
        return int(filename.split('_')[0])
    except ValueError:
        return float('inf')  # Si no es un número, colócalo al final

def procesar_archivo_html(ruta_html):
    # Lee el contenido del archivo HTML
    with open(ruta_html, 'r', encoding='utf-8') as file:
        html_content = file.read()
        # primera_linea = html_content.splitlines()[0]

    # Parsea el HTML usando BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extrae el Icon, título y el subtítulo
    # Verificar si existe el elemento 'icon'
    if hasattr(soup, 'icon') and soup.icon:
        icon = soup.icon.text.strip()
    else:
        icon = None  # Otra acción que desees realizar en caso de que no exista 'icon'

    svg = soup.find('svg', id='null53')
    if svg:
        svg = str(svg)
    else:
        svg = None
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
        'IconClass' : icon,
        'SVG': svg,
        'Title': title,
        'Subtitle': subtitle
    }

    # Convierte el diccionario a formato JSON
    json_result = json.dumps(result_dict, indent=2)

    # Construye la ruta completa al archivo JSON

    file_name_minuscula = os.path.basename(ruta_html).replace('.html', '.json')
    file_name_minuscula = file_name_minuscula.lower()


    ruta_json = os.path.join(os.path.dirname(ruta_html), file_name_minuscula)
    
    # Escribe el resultado en un archivo JSON
    with open(ruta_json, 'w', encoding='utf-8') as json_file:
        json_file.write(json_result)

    print(f"JSON generado con éxito para {os.path.basename(ruta_html)}.")

def procesar_json(json_path, carpeta_a_crear):
    with open(json_path, 'r') as file:
        # Obtener el tamaño del archivo
        file_size = os.path.getsize(json_path)
        
        if file_size == 0:
            print(f"El JSON {json_path} está vacío.")
            return
        data = json.load(file)

    filename = os.path.basename(json_path)
    if filename[0].isdigit():
        new_filename = filename.split('_')[1]
        new_filename = json_path.replace(filename, new_filename)
        # os.rename(json_path, new_filename)
        json_path = new_filename

    title = os.path.splitext(os.path.basename(json_path))[0].capitalize()

    # Dividir la ruta en partes utilizando '/'
    partes_ruta = json_path.split('/')
    # Obtener los últimos tres elementos
    if partes_ruta[-3][0].isdigit():
        partes_ruta[-3] = partes_ruta[-3].split('_')[1]
    ultimos_tres_elementos = '/'.join(partes_ruta[-3:])

    base_folder = carpeta_a_crear
    if not carpeta_a_crear.endswith('/'):
        base_folder  += '/'

    section = {
        "Href": base_folder + ultimos_tres_elementos.replace('.json', ''),
        "IconClass": data.get("Icon", ""),
        "SVG": data.get("SVG", ""),
        "Title": title,
        "Subtitle": data.get("Subtitle", "")
    }

    return section

def generar_json_general(carpeta_a_trabajar, carpeta_a_crear):
    result = {"Sections": []}

    for carpeta_actual, subcarpetas, archivos in os.walk(carpeta_a_trabajar):
        if carpeta_actual == carpeta_a_trabajar:
            for archivo in archivos:
                if archivo.endswith('.html'):
                    ruta_html = os.path.join(carpeta_actual, archivo)
                    procesar_archivo_html(ruta_html)
        if carpeta_actual != carpeta_a_trabajar:  # Excluir la carpeta raíz
            lista_ordenada = sorted(archivos, key=lambda x: extract_number_from_filename(x))
            # print(lista_ordenada)
            for archivo in lista_ordenada:
                if archivo.endswith('.json'):
                    json_path = os.path.join(carpeta_actual, archivo)
                    section = procesar_json(json_path, carpeta_a_crear)
                    result["Sections"].append(section)

    return result

def guardar_json_en_archivo(ruta_carpeta, json_data):

    for carpeta_actual, subcarpetas, archivos in os.walk(carpeta_a_trabajar):
        if carpeta_actual == carpeta_a_trabajar:
            for archivo in archivos:
                if archivo.endswith('.json'):
                    ruta_final = os.path.join(carpeta_actual, archivo)
                    with open(ruta_final, 'r') as archivo_json:
                        contenido_existente = json.load(archivo_json)
                    contenido_existente.update(json_data)
                    nuevo_contenido_json = json.dumps(contenido_existente, indent=2)
                    with open(ruta_final, 'w') as archivo_json:
                        archivo_json.write(nuevo_contenido_json)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python crear-json-general.py <carpeta_a_trabajar> <carpeta_a_crear>")
        sys.exit(1)

    carpeta_a_trabajar = sys.argv[1]
    carpeta_a_crear = sys.argv[2]

    if not os.path.isdir(carpeta_a_trabajar):
        print(f"La ruta proporcionada '{carpeta_a_trabajar}' no es una carpeta válida.")
        sys.exit(1)

    json_result = generar_json_general(carpeta_a_trabajar, carpeta_a_crear)

    if json_result["Sections"]:
        # Guardar el JSON en un archivo en la misma carpeta
        guardar_json_en_archivo(carpeta_a_trabajar, json_result)

        print(f"JSON generado y guardado en {carpeta_a_trabajar}/{os.path.basename(carpeta_a_trabajar)}.json")
    else:
        print("No se encontraron archivos json.")