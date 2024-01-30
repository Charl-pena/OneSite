import os
import re
import sys
import shutil
from pathlib import Path

def copiar_contenidos(carpeta_a_trabajar, carpeta_a_crear, folders_with_articles, original_folder_paths):
    new_base_path      = Path(carpeta_a_crear)
    original_base_path = Path(carpeta_a_trabajar)

    for i in range(len(folders_with_articles)):
        shutil.copytree(original_folder_paths[i], new_base_path / folders_with_articles[i], ignore=shutil.ignore_patterns('*.html') )
        print(f"carpeta {original_folder_paths[i]} copiada.")
    
        # Limpiar cadena
        ruta_limpia = original_folder_paths[i].replace("/articles", "")
        # Obtener la lista de archivos en la carpeta de origen
        archivos_en_origen = os.listdir(ruta_limpia)

        # Filtrar solo los archivos JSON en la carpeta de origen
        archivos_json = [archivo for archivo in archivos_en_origen if archivo.endswith('.json')]

            # Copiar los archivos JSON a la carpeta de destino
        for archivo_json in archivos_json:
            ruta_origen = os.path.join(ruta_limpia, archivo_json)
            ruta_destino = os.path.join(new_base_path, archivo_json)
            shutil.copy(ruta_origen, ruta_destino)
            print(f"JSON de Seccion {archivo_json} copiado.")

    menu_file = "menu.json"
    shutil.copy(os.path.join(original_base_path, menu_file), os.path.join(new_base_path, menu_file) )
    print(f"JSON {menu_file} copiado.")

def find_folders_with_articles(root_folder):
    folders_with_articles = []
    original_folder_paths = []
    for root, dirs, files in os.walk(root_folder):
        if "articles" in dirs:
            original_folder_paths.append(os.path.join(root, "articles"))
            parent_folder_name = os.path.basename(root)
            folders_with_articles.append(os.path.join(parent_folder_name, "articles"))

    return folders_with_articles, original_folder_paths

def delete_prefix_folders(directorio):
    for nombre_carpeta in os.listdir(directorio):
        ruta_carpeta = os.path.join(directorio, nombre_carpeta)
        # Patrón que debe cumplir el nombre de la carpeta
        patron = re.compile(r"\d+_")
        
        # Verifica si es una carpeta y si el fragmento 'd_' está en el nombre
        if os.path.isdir(ruta_carpeta):
            if patron.match(nombre_carpeta):  
                # Construye el nuevo nombre eliminando el fragmento 'd_'
                nuevo_nombre = nombre_carpeta.split('_')[1]
                
                # Construye la nueva ruta con el nuevo nombre
                nueva_ruta_carpeta = os.path.join(directorio, nuevo_nombre)
                 
                # Renombra la carpeta
                os.rename(ruta_carpeta, nueva_ruta_carpeta)
                print(f"Renombrada: {nombre_carpeta} -> {nuevo_nombre}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python organizar-files.py <carpeta_a_trabajar> <carpeta_a_crear>")
        sys.exit(1)

    carpeta_a_trabajar = sys.argv[1]
    carpeta_a_crear = sys.argv[2]

    if not os.path.isdir(carpeta_a_trabajar):
        print(f"La ruta proporcionada '{carpeta_a_trabajar}' no es una carpeta válida.")
        sys.exit(1)


    folders_with_articles, original_folder_paths = find_folders_with_articles(carpeta_a_trabajar)

    if folders_with_articles and original_folder_paths:
        if os.path.exists(carpeta_a_crear):
            shutil.rmtree(carpeta_a_crear)
        copiar_contenidos(carpeta_a_trabajar, carpeta_a_crear, folders_with_articles, original_folder_paths)
        delete_prefix_folders(carpeta_a_crear)
    else:
        print("No se encontraron carpetas con subcarpeta 'articles'.")
