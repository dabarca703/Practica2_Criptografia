# Reutilizamos las conversiones que ya hemos programado.
from basics import to_numbers, to_letters


def encrypt(plaintext: str, k: int) -> str:
    # Reducimos la clave al intervalo de 0 a 25.
    k = k % 26

    # Normalizamos el mensaje y convertimos sus letras en números.
    numbers = to_numbers(plaintext)

    # Creamos una lista para guardar los números cifrados.
    encrypted = []

    # Recorremos cada número del mensaje.
    for number in numbers:
        # Desplazamos la letra y volvemos al inicio si superamos la Z.
        shifted = (number + k) % 26

        # Guardamos el número cifrado.
        encrypted.append(shifted)

    # Convertimos los números cifrados en letras.
    return to_letters(encrypted)


def decrypt(ciphertext: str, k: int) -> str:
    # Reducimos la clave al intervalo de 0 a 25.
    k = k % 26

    # Convertimos las letras del mensaje cifrado en números.
    numbers = to_numbers(ciphertext)

    # Creamos una lista para guardar los números descifrados.
    decrypted = []

    # Recorremos cada número del mensaje cifrado.
    for number in numbers:
        # Restamos el desplazamiento para recuperar la letra original.
        shifted = (number - k) % 26

        # Guardamos el número descifrado.
        decrypted.append(shifted)

    # Convertimos los números recuperados en letras.
    return to_letters(decrypted)
