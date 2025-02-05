import boto3
import hashlib
import os
from dotenv import load_dotenv

def get_s3_file_metadata(bucket_name, file_key):
    # Crear una sesión de cliente S3
    s3 = boto3.client('s3')

    try:
        # Obtener los metadatos del objeto
        response = s3.head_object(Bucket=bucket_name, Key=file_key)
        
        # Imprimir metadatos básicos
        print("Metadata del archivo:")
        print(f"Tamaño del archivo: {response['ContentLength']} bytes")
        print(f"Tipo de contenido: {response['ContentType']}")
        print(f"Última modificación: {response['LastModified']}")
        print("Metadatos personalizados (si existen):")
        custom_metadata = response.get('Metadata', {})
        if custom_metadata:
            for key, value in custom_metadata.items():
                print(f"  {key}: {value}")
        else:
            print("  No hay metadatos personalizados.")
    
    except Exception as e:
        print(f"Error al obtener metadata del archivo: {e}")

# Cambiar estos valores por los de tu bucket S3
bucket_name = s.environ['BUCKET_NAME']
file_key = "ruta/del/archivo.txt"  # Ejemplo: carpeta/archivo.jpg

# Llamar a la función
get_s3_file_metadata(bucket_name, file_key)