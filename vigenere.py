# Importamos las conversiones que ya hemos implementado.
from basics import to_numbers, to_letters


def key_to_numbers(key: str) -> list[int]:
    # Rechazamos una clave vacía.
    if len(key) == 0:
        raise ValueError("La clave de Vigenere no puede estar vacía")

    # Solo aceptamos letras del alfabeto A-Z, en mayúsculas o minúsculas.
    for character in key:
        if not ("A" <= character <= "Z" or "a" <= character <= "z"):
            raise ValueError("La clave de Vigenere solo puede contener letras A-Z")

    # Convertimos las letras de la clave en desplazamientos.
    return to_numbers(key)


def encrypt(plaintext: str, key: str) -> str:
    # Validamos la clave y obtenemos sus desplazamientos.
    shifts = key_to_numbers(key)

    # Normalizamos el mensaje y convertimos sus letras en números.
    numbers = to_numbers(plaintext)

    # Creamos una lista para guardar los números cifrados.
    encrypted = []

    # Recorremos las posiciones del mensaje normalizado.
    for i in range(len(numbers)):
        # Repetimos la clave cuando llegamos a su final.
        shift = shifts[i % len(shifts)]

        # Sumamos el desplazamiento correspondiente a esta posición.
        encrypted_number = (numbers[i] + shift) % 26

        # Guardamos el número cifrado.
        encrypted.append(encrypted_number)

    # Convertimos los números cifrados en letras.
    return to_letters(encrypted)


def decrypt(ciphertext: str, key: str) -> str:
    # Validamos la clave y obtenemos sus desplazamientos.
    shifts = key_to_numbers(key)

    # Convertimos el mensaje cifrado en números.
    numbers = to_numbers(ciphertext)

    # Creamos una lista para guardar los números recuperados.
    decrypted = []

    # Recorremos las posiciones del mensaje cifrado.
    for i in range(len(numbers)):
        # Seleccionamos el desplazamiento que se usó al cifrar.
        shift = shifts[i % len(shifts)]

        # Restamos ese desplazamiento para recuperar la letra original.
        decrypted_number = (numbers[i] - shift) % 26

        # Guardamos el número recuperado.
        decrypted.append(decrypted_number)

    # Convertimos el resultado en letras.
    return to_letters(decrypted)


def cosets(ciphertext: str, m: int) -> list[str]:
    # La longitud de la clave debe ser un entero positivo.
    if not isinstance(m, int) or m <= 0:
        raise ValueError("La longitud m debe ser un entero positivo")

    # Normalizamos el texto para trabajar solo con letras A-Z.
    normalized = to_letters(to_numbers(ciphertext))

    # Creamos una lista donde guardaremos los grupos.
    groups = []

    # Creamos un grupo por cada posición de la clave.
    for i in range(m):
        # Tomamos una letra cada m posiciones, empezando por i.
        group = normalized[i::m]

        # Añadimos el grupo a la lista.
        groups.append(group)

    # Devolvemos los m grupos.
    return groups

