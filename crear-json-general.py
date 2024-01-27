import os
import json
import sys

# def procesar_cadena(input_str):
#     # Eliminar la subcadena "null53-"
#     processed_str = input_str.replace("null53-", "")

#     # Dividir la cadena en partes
#     partes = processed_str.split('/')

#     # Reorganizar las partes según el patrón deseado
#     output_str = "/".join([partes[0], partes[2], partes[4]])

#     return output_str

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
        "Subtitle": data.get("ActualSubtitle", "")
    }

    return section

def generar_json_general(carpeta_a_trabajar, carpeta_a_crear):
    result = {"Sections": []}

    for carpeta_actual, subcarpetas, archivos in os.walk(carpeta_a_trabajar):
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
    ruta_final = os.path.join(ruta_carpeta, nombre_archivo)

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