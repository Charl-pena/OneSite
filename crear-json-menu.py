import os
import sys
import json

def clean_section_name(section_name):
    return section_name.replace("null53-", "")

def generate_menu_json(root_path):
    menu_sections = []

    for section_name in os.listdir(root_path):
        section_path = os.path.join(root_path, section_name)

        if os.path.isdir(section_path):
            cleaned_section_name = clean_section_name(section_name)
            menu_section = {"NameSection": cleaned_section_name, "MenuItems": []}

            for item_name in os.listdir(section_path):
                item_path = os.path.join(section_path, item_name)

                if os.path.isdir(item_path):
                    submenus = []
                    for submenu_name in os.listdir(item_path):
                        submenu_path = os.path.join(item_path, submenu_name)
                        
                        if os.path.isdir(submenu_path):
                            submenu_items = []
                            for article_name in os.listdir(submenu_path):
                                article_path = os.path.join(submenu_path, article_name)
                                if ".html" not in article_name:
                                    if os.path.isfile(article_path):
                                        article_title, article_extension = os.path.splitext(article_name)
                                        article_href = f"/documentation/{item_name.lower()}/{submenu_name.lower()}/{article_title.lower()}/"
                                        article = {"Title": article_title.capitalize(), "Href": article_href}
                                        submenu_items.append(article)

                    menu_item = {"Title": item_name.capitalize(), "Href": f"/documentation/{item_name.lower()}/", "SubMenus": submenu_items}
                    menu_section["MenuItems"].append(menu_item)

            menu_sections.append(menu_section)

    menu_json = {"MenuSections": menu_sections}
    return json.dumps(menu_json, indent=2)

def guardar_json_en_archivo(ruta_carpeta, result_json, file_name):
    ruta_final = os.path.join(ruta_carpeta, file_name)

    with open(ruta_final, 'w') as file:
        file.write(result_json)

    print(f"JSON generado con éxito. Puedes encontrarlo en '{ruta_final}'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python crear-json-menu.py <ruta_de_tu_carpeta>")
        sys.exit(1)

    ruta_de_tu_carpeta = sys.argv[1]

    if not os.path.isdir(ruta_de_tu_carpeta):
        print(f"La ruta proporcionada '{ruta_de_tu_carpeta}' no es una carpeta válida.")
        sys.exit(1)

    name_json = "menu.json"
    result_json = generate_menu_json(ruta_de_tu_carpeta)
    if result_json:
        # Guardar el JSON en un archivo en la misma carpeta
        guardar_json_en_archivo(ruta_de_tu_carpeta, result_json, name_json)
    else:
        print("menu.json no se pudo generar, no hay informacion necesaria.")
