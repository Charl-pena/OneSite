import os
import sys
import subprocess

def find_folders_with_articles_and_parent(carpeta_a_trabajar):
    folders_with_articles = []
    parent_folders_articles = []

    for root, dirs, files in os.walk(carpeta_a_trabajar):
        if "articles" in dirs:

            parent_folders_articles.append(root)
            folders_with_articles.append(os.path.join(root, "articles"))

    return folders_with_articles, parent_folders_articles

def ejecutar_scripts(carpeta_a_trabajar, carpeta_a_crear, folders_with_articles, parent_folders_articles ):
    for folder in folders_with_articles:
        # Ruta al script crear-json-particular
        ruta_script = "./crear-json-particular.py"

        # Ejecutar el script crear-json-particular
        subprocess.run(["python3", ruta_script, folder])
    
    for folder in parent_folders_articles:
        # Ruta al script crear-json-general
        ruta_script = "./crear-json-general.py"

        # Ejecutar el script crear-json-general
        subprocess.run(["python3", ruta_script, folder, carpeta_a_crear])
    
    # Ejecutar el script crear-json-menu
    ruta_script = "./crear-json-menu.py"
    subprocess.run(["python3", ruta_script, carpeta_a_trabajar, carpeta_a_crear])

    # Ejecutar el script organizar-files
    ruta_script = "./organizar-files.py"
    subprocess.run(["python3", ruta_script, carpeta_a_trabajar, carpeta_a_crear])

    # Ejecutar el script crear-json-general
    ruta_script = "./crear-json-general.py"
    subprocess.run(["python3", ruta_script, carpeta_a_crear, carpeta_a_crear])



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python masterhand.py <carpeta_a_trabajar> <carpeta_a_crear>")
        sys.exit(1)

    carpeta_a_trabajar = sys.argv[1]
    carpeta_a_crear = sys.argv[2]

    if not os.path.isdir(carpeta_a_trabajar):
        print(f"La ruta proporcionada '{carpeta_a_trabajar}' no es una carpeta válida.")
        sys.exit(1)


    folders_with_articles, parent_folders_articles = find_folders_with_articles_and_parent(carpeta_a_trabajar)

    if folders_with_articles and parent_folders_articles:
        ejecutar_scripts(carpeta_a_trabajar, carpeta_a_crear, folders_with_articles, parent_folders_articles)
    else:
        print("No se encontraron carpetas con subcarpeta 'articles'.")
