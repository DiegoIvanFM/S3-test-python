import hashlib
import io
from webdav4.client import Client

# Configurar el cliente WebDAV
webdav_url = "http://webdav.server.com/"
username = "usuario"
password = "contraseña"

client = Client(webdav_url, auth=(username, password))

# Archivo a subir
archivo = "archivo.txt"
ruta_webdav = f"ruta/{archivo}"
ruta_checksum = f"{ruta_webdav}.sha256"

# Función para calcular SHA-256 de un archivo
def calcular_sha256(filename):
    hasher = hashlib.sha256()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

# 1. Subir el archivo
client.upload_file(archivo, ruta_webdav)
print(f"📤 Archivo {archivo} subido a {ruta_webdav}")

# 2. Calcular el checksum y guardarlo en WebDAV
checksum = calcular_sha256(archivo)
checksum_data = io.BytesIO(checksum.encode())  # Convertir string a BytesIO
client.upload_fileobj(checksum_data, ruta_checksum)
print(f"✅ Checksum SHA-256 ({checksum}) subido a {ruta_checksum}")

# 3. Descargar el archivo desde WebDAV y validar integridad
client.download_file(ruta_webdav, "archivo_descargado.txt")
checksum_descargado = calcular_sha256("archivo_descargado.txt")

# 4. Descargar el checksum desde WebDAV
with io.BytesIO() as downloaded_data:
    client.download_fileobj(ruta_checksum, downloaded_data)
    downloaded_data.seek(0)
    checksum_guardado = downloaded_data.read().decode().strip()

# 5. Verificar integridad
if checksum_descargado == checksum_guardado:
    print("✅ El archivo es íntegro. Coincide el checksum.")
else:
    print("❌ ¡Error! El archivo ha sido modificado o corrupto.")
