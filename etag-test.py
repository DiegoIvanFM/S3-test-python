import boto3
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

def calcular_md5(archivo):
    md5 = hashlib.md5()
    with open(archivo, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()

# Crear cliente S3
s3 = boto3.client('s3',
                        aws_access_key_id=os.environ['ACCESS_KEY'],
                        aws_secret_access_key=os.environ['SECRET_KEY'])

bucket_name =os.environ['BUCKET_NAME']
key ="algo/prueba.txt"
archivo_local = 'prueba.txt'

# Subir archivo
s3.upload_file(archivo_local, bucket_name, key)

# Calcular MD5 localmente
md5_local = calcular_md5(archivo_local)
print ("Hash local: ", md5_local)

# Obtener ETag del objeto en S3
response = s3.head_object(Bucket=bucket_name, Key=key)
etag = response['ETag'].strip('"')
print("etag de server: ", etag)

# Verificar integridad
if md5_local == etag:
    print("La carga fue exitosa y el archivo es íntegro.")
    print ("Hash local: ", md5_local)
    print("etag de server: ", response)
else:
    print("El archivo puede estar corrupto o el ETag no es un hash MD5 simple.")
    print ("Hash local: ", md5_local)
    print("etag de server: ", etag)