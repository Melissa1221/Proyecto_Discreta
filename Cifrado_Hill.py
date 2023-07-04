import numpy as np
import sympy as sp

# Función para generar una matriz clave aleatoria invertible
def generate_key(n):
    while True:
        key = np.random.randint(0, 27, size=(n, n))
        det = int(np.round(np.linalg.det(key))) % 27
        try:
            det_inv = sp.mod_inverse(det, 27)
            return key
        except ValueError:
            pass

# Función para cifrar un mensaje usando la matriz clave
def encrypt(plaintext, key):
    n = key.shape[0]
    plaintext = plaintext.upper()  # Convertir a mayúsculas
    plaintext = [ord(c) - ord("A") if c != ' ' else 26 for c in plaintext]  # Convertir caracteres a números
    plaintext = np.array(plaintext)
    ciphertext = ""
    for i in range(0, len(plaintext), n):
        block = plaintext[i:i + n]
        if len(block) < n:
            block = np.append(block, [26]*(n - len(block)))  # Rellenar con 26s si el bloque es menor a n
        block = np.dot(key, block) % 27
        block = [chr(int(c) + ord("A")) if c != 26 else ' ' for c in block]  # Convertir números a caracteres
        ciphertext += "".join(block)
    return ciphertext

# Función para descifrar un mensaje usando la matriz clave
def decrypt(ciphertext, key):
    n = key.shape[0]
    ciphertext = [ord(c) - ord("A") if c != ' ' else 26 for c in ciphertext]  # Convertir caracteres a números
    ciphertext = np.array(ciphertext)
    decrypted_text = ""
    key_inv = sp.Matrix(key.tolist()).inv_mod(27).tolist()  # Calcular la matriz inversa de la clave
    key_inv = [[int(x) % 27 for x in row] for row in key_inv]
    key_inv = np.array(key_inv)
    print("Inverso Modular de la Matriz clave:\n",key_inv)
    for i in range(0, len(ciphertext), n):
        block = ciphertext[i:i + n]
        block = np.dot(key_inv, block) % 27
        block = [chr(int(c) + ord("A")) if c != 26 else ' ' for c in block]  # Convertir números a caracteres
        decrypted_text += "".join(block)
    return decrypted_text.strip()  # Eliminar espacios al final

# Obtener la palabra a cifrar por teclado
plaintext = input("Ingrese la palabra a cifrar: ")
key_size = int(input("Ingrese la dimension de la matriz clave: "))
# Generar una matriz clave aleatoria de tamaño nxn
key = generate_key(key_size)

print("Matriz clave:")
print(key)

ciphertext = encrypt(plaintext, key)
print("Texto cifrado:", ciphertext)

decrypted_text = decrypt(ciphertext, key)
print("Texto descifrado:", decrypted_text)
