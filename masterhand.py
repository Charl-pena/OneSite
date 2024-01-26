import os
import sys
import subprocess

def find_folders_with_articles_and_parent(root_folder):
    folders_with_articles = []
    parent_folders_articles = []

    for root, dirs, files in os.walk(root_folder):
        if "articles" in dirs:

            parent_folders_articles.append(root)
            folders_with_articles.append(os.path.join(root, "articles"))

    return folders_with_articles, parent_folders_articles

def ejecutar_scripts(root_folder, folders_with_articles, parent_folders_articles ):
    for folder in folders_with_articles:
        # Ruta al script secundario
        ruta_script = "./crear-json-particular.py"

        # Ejecutar el script secundario
        subprocess.run(["python3", ruta_script, folder])
    
    for folder in parent_folders_articles:
        # Ruta al script secundario
        ruta_script = "./crear-json-general.py"

        # Ejecutar el script secundario
        subprocess.run(["python3", ruta_script, folder])
    
    ruta_script = "./crear-json-menu.py"

    # Ejecutar el script secundario
    subprocess.run(["python3", ruta_script, root_folder])

    ruta_script = "./organizar-files.py"

    # Ejecutar el script secundario
    subprocess.run(["python3", ruta_script, root_folder])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python masterhand.py <ruta_de_tu_carpeta>")
        sys.exit(1)

    ruta_de_tu_carpeta = sys.argv[1]

    if not os.path.isdir(ruta_de_tu_carpeta):
        print(f"La ruta proporcionada '{ruta_de_tu_carpeta}' no es una carpeta válida.")
        sys.exit(1)


    folders_with_articles, parent_folders_articles = find_folders_with_articles_and_parent(ruta_de_tu_carpeta)

    if folders_with_articles and parent_folders_articles:
        ejecutar_scripts(ruta_de_tu_carpeta, folders_with_articles, parent_folders_articles)
    else:
        print("No se encontraron carpetas con subcarpeta 'articles'.")
