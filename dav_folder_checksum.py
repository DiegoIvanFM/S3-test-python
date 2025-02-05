import hashlib
import os
import io
from webdav4.client import Client

# Configurar el cliente WebDAV
webdav_url = "http://webdav.server.com/"
username = "usuario"
password = "contraseña"

client = Client(webdav_url, auth=(username, password))

# Carpeta local y remota en WebDAV
carpeta_local = "mi_carpeta"
carpeta_remota = f"ruta/{carpeta_local}"
ruta_checksums = f"{carpeta_remota}/checksums.txt"

# Función para calcular SHA-256 en streaming
def calcular_sha256_stream(file_obj, chunk_size=8192):
    """Calcula el SHA-256 de un archivo en chunks."""
    hasher = hashlib.sha256()
    while chunk := file_obj.read(chunk_size):
        hasher.update(chunk)
    return hasher.hexdigest()

# 1️⃣ Subir la carpeta a WebDAV
def subir_carpeta(client, carpeta_local, carpeta_remota):
    """Sube una carpeta y todos sus archivos a WebDAV."""
    for root, _, files in os.walk(carpeta_local):
        for file in files:
            ruta_local = os.path.join(root, file)
            ruta_webdav = f"{carpeta_remota}/{os.path.relpath(ruta_local, carpeta_local)}"
            client.upload_file(ruta_local, ruta_webdav)
            print(f"📤 Archivo subido: {ruta_webdav}")

subir_carpeta(client, carpeta_local, carpeta_remota)

# 2️⃣ Calcular checksums de los archivos en WebDAV y guardarlos en un diccionario
checksums = {}

def calcular_checksums_webdav(client, carpeta_remota):
    """Calcula los SHA-256 de todos los archivos en una carpeta en WebDAV."""
    for item in client.ls(carpeta_remota):
        if item["isdir"]:
            continue  # Saltar subcarpetas

        ruta_archivo = item["path"]
        with client.open(ruta_archivo, "rb") as remote_file:
            checksums[ruta_archivo] = calcular_sha256_stream(remote_file)

calcular_checksums_webdav(client, carpeta_remota)

# 3️⃣ Guardar los checksums en un archivo en WebDAV
checksums_str = "\n".join(f"{ruta} {checksum}" for ruta, checksum in checksums.items())
checksum_data = io.BytesIO(checksums_str.encode())
client.upload_fileobj(checksum_data, ruta_checksums)
print(f"✅ Archivo de checksums subido a {ruta_checksums}")

# 4️⃣ Descargar los archivos de WebDAV y recalcular sus checksums
checksums_descargados = {}

def calcular_checksums_descarga(client, carpeta_remota):
    """Calcula los SHA-256 de los archivos después de descargarlos."""
    for item in client.ls(carpeta_remota):
        if item["isdir"]:
            continue

        ruta_archivo = item["path"]
        with client.open(ruta_archivo, "rb") as remote_file:
            checksums_descargados[ruta_archivo] = calcular_sha256_stream(remote_file)

calcular_checksums_descarga(client, carpeta_remota)

# 5️⃣ Descargar el archivo de checksums y comparar
with io.BytesIO() as downloaded_data:
    client.download_fileobj(ruta_checksums, downloaded_data)
    downloaded_data.seek(0)
    checksums_guardados = {
        line.split(" ")[0]: line.split(" ")[1]
        for line in downloaded_data.read().decode().splitlines()
    }

# Verificar integridad de los archivos
errores = []
for ruta, checksum in checksums_descargados.items():
    if checksums_guardados.get(ruta) != checksum:
        errores.append(ruta)

if not errores:
    print("✅ Todos los archivos son íntegros.")
else:
    print("❌ ¡Error! Los siguientes archivos han sido modificados o están corruptos:")
    for error in errores:
        print(f"   - {error}")
