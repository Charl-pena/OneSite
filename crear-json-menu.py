import os
import sys
import json

def clean_section_name(section_name):
    return section_name.replace("null53-", "")

def extraer_info_json(json_necesario):
	with open(json_necesario, 'r') as file:
		# Obtener el tamaño del archivo
		file_size = os.path.getsize(json_necesario)
		
		if file_size == 0:
			print(f"El JSON {json_path} está vacío.")
			return
		data = json.load(file)
	icon_class = data["IconClass"]
	return icon_class

def generate_menu_json(root_path, carpeta_a_crear):
    menu_sections = []

    base_folder = carpeta_a_crear
    if not carpeta_a_crear.endswith('/'):
        base_folder  += '/'

    for section_name in os.listdir(root_path):
        section_path = os.path.join(root_path, section_name)

        if os.path.isdir(section_path):
            cleaned_section_name = clean_section_name(section_name)
            menu_section = {"NameSection": cleaned_section_name, "MenuItems": []}

            for item_name in os.listdir(section_path):
                item_path = os.path.join(section_path, item_name)
                iconClass = ""
                if os.path.isdir(item_path):
                    submenus = []
                    for submenu_name in os.listdir(item_path):
                        submenu_path = os.path.join(item_path, submenu_name)
                        if ".json" in submenu_name:
                            iconClass = extraer_info_json(submenu_path) 
                            # print(extraer_info_json(submenu_path))
                        if os.path.isdir(submenu_path):
                            submenu_items = []
                            for article_name in os.listdir(submenu_path):
                                article_path = os.path.join(submenu_path, article_name)
                                if ".html" not in article_name:
                                    if os.path.isfile(article_path):
                                        article_title, article_extension = os.path.splitext(article_name)
                                        article_href = f"{base_folder}{item_name.lower()}/{submenu_name.lower()}/{article_title.lower()}/"
                                        article = {"Title": article_title.capitalize(), "Href": article_href}
                                        submenu_items.append(article)

                    menu_item = {"Title": item_name.capitalize(), "Href": f"{base_folder}{item_name.lower()}/", "IconClass" : iconClass, "SubMenus": submenu_items}
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
    if len(sys.argv) != 3:
        print("Uso: python crear-json-menu.py <carpeta_a_trabajar> <carpeta_a_crear>")
        sys.exit(1)

    carpeta_a_trabajar = sys.argv[1]
    carpeta_a_crear = sys.argv[2]

    if not os.path.isdir(carpeta_a_trabajar):
        print(f"La ruta proporcionada '{carpeta_a_trabajar}' no es una carpeta válida.")
        sys.exit(1)


    name_json = "menu.json"
    result_json = generate_menu_json(carpeta_a_trabajar, carpeta_a_crear)
    if result_json:
        # Guardar el JSON en un archivo en la misma carpeta
        guardar_json_en_archivo(carpeta_a_trabajar, result_json, name_json)
    else:
        print("menu.json no se pudo generar, no hay informacion necesaria.")
