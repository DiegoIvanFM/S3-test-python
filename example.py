import requests

# Credenciales y URL base
BASE_URL = "https://<tu_servidor>/api/v2"
USERNAME = "admin"
PASSWORD = "admin_password"

# Obtener token
def get_token():
    response = requests.post(f"{BASE_URL}/token", json={"username": USERNAME, "password": PASSWORD})
    response.raise_for_status()
    return response.json()["access_token"]

# Obtener checksum de un archivo
def get_checksum(token, bucket_path, filename):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/files/{bucket_path}/{filename}?checksum=true", headers=headers)
    response.raise_for_status()
    return response.json()

# Uso
token = get_token()
file_info = get_checksum(token, "mi_bucket", "archivo1.txt")
print(f"Checksum de archivo1.txt: {file_info['checksum']}")
