import os
import sys
import json

def crear_json(json_necesario, nombre_del_json):
	with open(json_necesario, 'r') as file:
		# Obtener el tamaño del archivo
		file_size = os.path.getsize(json_necesario)
		
		if file_size == 0:
			print(f"El JSON {json_path} está vacío.")
			return
		data = json.load(file)

	menu_items_without_submenus = []

	for section in data['MenuSections']:
		for menu_item in section['MenuItems']:
			menu_item_without_submenus = {k: v for k, v in menu_item.items() if k != 'SubMenus'}
			menu_items_without_submenus.append(menu_item_without_submenus)

	result_data = {"Sections": menu_items_without_submenus}
	nombre_del_json = os.path.normpath(nombre_del_json)
	json_path = os.path.join(nombre_del_json, nombre_del_json) 
	with open(f"{json_path}.json", 'w') as output_file:
		json.dump(result_data, output_file, indent=2)

	print(f"Data has been saved to '{nombre_del_json}.json'")

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Uso: python crear-documentation.py <json_necesario.json>, <nombre_del_json")
		sys.exit(1)
  	
	json_necesario  = sys.argv[1]
	carpeta_a_crear = sys.argv[2]

	if not os.path.exists(json_necesario):
		print(f"La ruta proporcionada '{json_necesario}' no es un json válido.")
		sys.exit(1)

	if not os.path.isdir(carpeta_a_crear):
		print(f"La ruta proporcionada '{carpeta_a_crear}' no es una carpeta válida.")
		sys.exit(1)
	
	crear_json(json_necesario, carpeta_a_crear)