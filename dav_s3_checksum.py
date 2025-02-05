import hashlib
from webdav4.client import Client
import boto3

# Configuración de WebDAV
webdav_url = 'https://your-webdav-server.com'
webdav_username = 'your-username'
webdav_password = 'your-password'

# Configuración de S3
s3_client = boto3.client('s3')
bucket_name = 'your-bucket-name'

# Ruta del archivo local
file_path = 'path/to/your/file.txt'

# Calcular el checksum SHA-256
def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

checksum = calculate_sha256(file_path)
print(f"Checksum SHA-256 del archivo: {checksum}")

# Subir el archivo a WebDAV
webdav_client = Client(webdav_url, auth=(webdav_username, webdav_password))
remote_path = 'remote/path/file.txt'

with open(file_path, 'rb') as file:
    webdav_client.upload(file, remote_path)

print(f"Archivo subido a WebDAV en: {remote_path}")

# Almacenar el checksum en S3 como metadata
s3_client.put_object_tagging(
    Bucket=bucket_name,
    Key=remote_path,
    Tagging={
        'TagSet': [
            {
                'Key': 'SHA256Checksum',
                'Value': checksum
            },
        ]
    }
)

print("Checksum almacenado como metadata en S3.")