import hashlib

def calcular_sha256(filename, chunk_size=8192):
    """Calcula el SHA-256 de un archivo en bloques para evitar alto consumo de memoria."""
    hasher = hashlib.sha256()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):  # Leer en bloques
            hasher.update(chunk)  # Actualizar hash con cada chunk
    return hasher.hexdigest()

# Ejemplo de uso con un archivo grande
archivo_pesado = "archivo_grande.dat"
checksum = calcular_sha256(archivo_pesado)
print(f"SHA-256: {checksum}")
