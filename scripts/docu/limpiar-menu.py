import os
import sys
import json

def limpiar_menu(json_necesario):
    with open(json_necesario, 'r') as file:
     # Obtener el tamaño del archivo
     file_size = os.path.getsize(json_necesario)

     if file_size == 0:
         print(f"El JSON {json_necesario} está vacío.")
         return
     data = json.load(file)

   # Verificar si hay secciones y si tienen un objeto "Subtitle"
    if 'MenuSections' in data and isinstance(data['MenuSections'], list):
       for menuSection in data['MenuSections']:
          if 'MenuItems' in menuSection:
                for menuItems in menuSection['MenuItems']:
                   if 'Subtitle' in menuItems:
                      del menuItems['Subtitle']
    # Convertir el diccionario modificado de nuevo a JSON
    json_result = json.dumps(data, indent=2)

    # Escribir el nuevo contenido JSON de vuelta al archivo
    with open(json_necesario, 'w') as archivo_json:
       archivo_json.write(json_result)
    
    print(f"El archivo {json_necesario} se ha limpiado correctamente");

if __name__ == "__main__":
   if len(sys.argv) != 2:
       print("Uso: python limpiar-menu.py <json_necesario>")
       sys.exit(1)

   json_necesario = sys.argv[1]

   if not os.path.exists(json_necesario):
       print(f"La ruta proporcionada '{json_necesario}' no es un json válido.")
       sys.exit(1)

   limpiar_menu(json_necesario)


