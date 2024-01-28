import os
import sys
import glob

def eliminar_archivos_json(carpeta):
   # Obtener la lista de archivos JSON en la carpeta y subcarpetas
   archivos_json = glob.glob(os.path.join(carpeta, '**', '*.json'), recursive=True)

   # Eliminar cada archivo encontrado
   for archivo in archivos_json:
      try:
          os.remove(archivo)
          print(f"Archivo eliminado: {archivo}")
      except OSError as e:
          print(f"No se pudo eliminar {archivo}: {e}")

if __name__ == "__main__":
   if len(sys.argv) != 2:
       print("Uso: python organizar-files.py <carpeta_a_limpiar>")
       sys.exit(1)

   carpeta_a_limpiar = sys.argv[1]

   if not os.path.isdir(carpeta_a_limpiar):
       print(f"La ruta proporcionada '{carpeta_a_limpiar}' no es una carpeta válida.")
       sys.exit(1)

   eliminar_archivos_json(carpeta_a_limpiar)