import hashlib
import io
from webdav4.client import Client

# Configurar el cliente WebDAV
webdav_url = "http://webdav.server.com/"
username = "usuario"
password = "contraseña"

client = Client(webdav_url, auth=(username, password))

# Archivo local y rutas en WebDAV
archivo_local = "archivo_grande.dat"
archivo_remoto = f"ruta/{archivo_local}"
ruta_checksum = f"{archivo_remoto}.sha256"

# Función para calcular SHA-256 en streaming
def calcular_sha256_stream(file_obj, chunk_size=8192):
    """Calcula el SHA-256 de un archivo en chunks."""
    hasher = hashlib.sha256()
    while chunk := file_obj.read(chunk_size):
        hasher.update(chunk)
    return hasher.hexdigest()

# 1️⃣ Subir el archivo a WebDAV
client.upload_file(archivo_local, archivo_remoto)
print(f"📤 Archivo subido a WebDAV: {archivo_remoto}")

# 2️⃣ Calcular el checksum directamente en WebDAV en chunks
with client.open(archivo_remoto, "rb") as remote_file:
    checksum_webdav = calcular_sha256_stream(remote_file)
print(f"📌 Checksum calculado en WebDAV: {checksum_webdav}")

# 3️⃣ Guardar el checksum en WebDAV
checksum_data = io.BytesIO(checksum_webdav.encode())
client.upload_fileobj(checksum_data, ruta_checksum)
print(f"✅ Checksum guardado en WebDAV en {ruta_checksum}")

# 4️⃣ Descargar el archivo y calcular su checksum en streaming
with client.open(archivo_remoto, "rb") as downloaded_file:
    checksum_descargado = calcular_sha256_stream(downloaded_file)
print(f"🔍 Checksum calculado después de la descarga: {checksum_descargado}")

# 5️⃣ Descargar el checksum guardado en WebDAV
with io.BytesIO() as downloaded_data:
    client.download_fileobj(ruta_checksum, downloaded_data)
    downloaded_data.seek(0)
    checksum_guardado = downloaded_data.read().decode().strip()

# 6️⃣ Verificar integridad del archivo
if checksum_descargado == checksum_guardado:
    print("✅ El archivo es íntegro. Coincide el checksum.")
else:
    print("❌ ¡Error! El archivo ha sido modificado o corrupto.")
