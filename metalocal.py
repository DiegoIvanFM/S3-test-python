import os
import time
from PIL import Image
from PIL.ExifTags import TAGS

def read_metadata(file_path):
    if not os.path.exists(file_path):
        print(f"El archivo '{file_path}' no existe.")
        return
    
    # Metadata básica del archivo
    print("Metadata básica:")
    metadata = os.stat(file_path)
    print(f"Nombre del archivo: {os.path.basename(file_path)}")
    print(f"Tamaño (bytes): {metadata.st_size}")
    print(f"Fecha de creación: {time.ctime(metadata.st_ctime)}")
    print(f"Última modificación: {time.ctime(metadata.st_mtime)}")
    print(f"Último acceso: {time.ctime(metadata.st_atime)}")
    print("-" * 40)
    
    # Si es una imagen, obtener metadata EXIF
    try:
        print("Metadata EXIF (si es una imagen):")
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    print(f"{tag}: {value}")
            else:
                print("No se encontraron datos EXIF.")
    except Exception as e:
        print(f"Error al procesar EXIF: {e}")
    print("-" * 40)

# Ruta del archivo
file_path = "C:/Projects/S3-test-python/anya_test_downloaded.jpg"  # Cambiar por la ruta real

# Llamar a la función
read_metadata(file_path)
