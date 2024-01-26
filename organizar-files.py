import os
import sys
import shutil
from pathlib import Path

def copiar_contenidos(original_base_folder, new_base_folder, folders_with_articles, original_folder_paths):
    new_base_path      = Path(new_base_folder)
    original_base_path = Path(original_base_folder)

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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python organizar-files.py <ruta_de_tu_carpeta>")
        sys.exit(1)

    ruta_de_tu_carpeta = sys.argv[1]

    if not os.path.isdir(ruta_de_tu_carpeta):
        print(f"La ruta proporcionada '{ruta_de_tu_carpeta}' no es una carpeta válida.")
        sys.exit(1)


    folders_with_articles, original_folder_paths = find_folders_with_articles(ruta_de_tu_carpeta)
    carpeta_base_nueva = "documentation"

    if folders_with_articles and original_folder_paths:
        if os.path.exists(carpeta_base_nueva):
            shutil.rmtree(carpeta_base_nueva)
        copiar_contenidos(ruta_de_tu_carpeta, carpeta_base_nueva, folders_with_articles, original_folder_paths)
    else:
        print("No se encontraron carpetas con subcarpeta 'articles'.")
