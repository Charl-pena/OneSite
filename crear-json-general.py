import os
import json
import sys
from bs4 import BeautifulSoup
# def procesar_cadena(input_str):
#     # Eliminar la subcadena "null53-"
#     processed_str = input_str.replace("null53-", "")

#     # Dividir la cadena en partes
#     partes = processed_str.split('/')

#     # Reorganizar las partes según el patrón deseado
#     output_str = "/".join([partes[0], partes[2], partes[4]])

#     return output_str

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
        'IconClass' : icon,
        'Title': title,
        'Subtitle': subtitle
    }

    # Convierte el diccionario a formato JSON
    json_result = json.dumps(result_dict, indent=2)

    # Construye la ruta completa al archivo JSON

    ruta_json = ruta_html.replace('.html', '.json')
    ruta_json = os.path.basename(ruta_json)
    ruta_json = ruta_json[0].lower() + ruta_json[1:]
    ruta_json = os.path.join(os.path.dirname(ruta_html), ruta_json) 
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

    title = os.path.splitext(os.path.basename(json_path))[0].capitalize()

    # Dividir la ruta en partes utilizando '/'
    partes_ruta = json_path.split('/')
    # Obtener los últimos tres elementos
    ultimos_tres_elementos = '/'.join(partes_ruta[-3:])

    base_folder = carpeta_a_crear
    if not carpeta_a_crear.endswith('/'):
        base_folder  += '/'

    section = {
        "Href": base_folder + ultimos_tres_elementos.replace('.json', ''),
        "IconClass": data.get("Icon", ""),
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
            for archivo in archivos:
                if archivo.endswith('.json'):
                    json_path = os.path.join(carpeta_actual, archivo)
                    section = procesar_json(json_path, carpeta_a_crear)
                    result["Sections"].append(section)

    return result

def guardar_json_en_archivo(ruta_carpeta, json_data):

    nombre_carpeta = os.path.basename(os.path.normpath(ruta_carpeta))
    nombre_archivo = f"{nombre_carpeta}.json"
    nombre_archivo = nombre_archivo[0].lower() + nombre_archivo[1:]
    ruta_final = os.path.join(ruta_carpeta, nombre_archivo)
    
    if os.path.exists(ruta_final):
        with open(ruta_final, 'r') as archivo_json:
            contenido_existente = json.load(archivo_json)

        contenido_existente.update(json_data)

        # Paso 3: Serializar el diccionario de Python a formato JSON
        nuevo_contenido_json = json.dumps(contenido_existente, indent=2)
    
        # Paso 4: Escribir el nuevo contenido JSON de vuelta al archivo
        with open(ruta_final, 'w') as archivo_json:
            archivo_json.write(nuevo_contenido_json)
    else:
        with open(ruta_final, 'w') as file:
            json.dump(json_data, file, indent=2)

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