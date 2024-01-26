import os
import json
import sys

def procesar_cadena(input_str):
    # Eliminar la subcadena "null53-"
    processed_str = input_str.replace("null53-", "")

    # Dividir la cadena en partes
    partes = processed_str.split('/')

    # Reorganizar las partes según el patrón deseado
    output_str = "/".join([partes[0], partes[2], partes[4]])

    return output_str

def procesar_json(json_path):
    with open(json_path, 'r') as file:
        # Obtener el tamaño del archivo
        file_size = os.path.getsize(json_path)
        
        if file_size == 0:
            print(f"El JSON {json_path} está vacío.")
            return
        data = json.load(file)

    title = os.path.splitext(os.path.basename(json_path))[0].capitalize()

    # Obtener el relative path del JSON en relación con la ubicación del script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    relative_path = os.path.relpath(json_path, script_dir)

    section = {
        "Href": procesar_cadena(relative_path.replace('.json', '')),
        "IconClass": data.get("Icon", ""),
        "Title": title,
        "Subtitle": data.get("ActualSubtitle", "")
    }

    return section

def generar_json_general(carpeta):
    result = {"Sections": []}

    for carpeta_actual, subcarpetas, archivos in os.walk(carpeta):
        if carpeta_actual != carpeta:  # Excluir la carpeta raíz
            for archivo in archivos:
                if archivo.endswith('.json'):
                    json_path = os.path.join(carpeta_actual, archivo)
                    section = procesar_json(json_path)
                    result["Sections"].append(section)

    return result

def guardar_json_en_archivo(ruta_carpeta, json_data):
    nombre_carpeta = os.path.basename(os.path.normpath(ruta_carpeta))
    nombre_archivo = f"{nombre_carpeta}.json"
    ruta_final = os.path.join(ruta_carpeta, nombre_archivo)

    with open(ruta_final, 'w') as file:
        json.dump(json_data, file, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python crear-json-general.py <ruta_de_tu_carpeta>")
        sys.exit(1)

    ruta_de_tu_carpeta = sys.argv[1]

    if not os.path.isdir(ruta_de_tu_carpeta):
        print(f"La ruta proporcionada '{ruta_de_tu_carpeta}' no es una carpeta válida.")
        sys.exit(1)

    json_result = generar_json_general(ruta_de_tu_carpeta)

    if json_result["Sections"]:
        # Guardar el JSON en un archivo en la misma carpeta
        guardar_json_en_archivo(ruta_de_tu_carpeta, json_result)

        print(f"JSON generado y guardado en {ruta_de_tu_carpeta}/{os.path.basename(ruta_de_tu_carpeta)}.json")
    else:
        print("No se encontraron archivos json.")