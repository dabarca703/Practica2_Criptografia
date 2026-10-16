# Importamos las funciones para convertir entre letras y números.
from basics import to_numbers, to_letters


# Definimos el alfabeto que utiliza la práctica.
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def validate_key(key: str) -> None:
    # La clave debe tener 26 caracteres y contener exactamente las letras A-Z.
    if len(key) != 26 or set(key) != set(ALPHABET):
        raise ValueError(
            "La clave debe contener las 26 letras A-Z en mayúsculas, sin repetir"
        )


def encrypt(plaintext: str, key: str) -> str:
    # Comprobamos que la clave sea una permutación válida del alfabeto.
    validate_key(key)

    # Normalizamos el mensaje y convertimos sus letras en posiciones.
    numbers = to_numbers(plaintext)

    # Creamos el texto donde guardaremos el resultado.
    ciphertext = ""

    # Recorremos las posiciones de las letras originales.
    for number in numbers:
        # Elegimos la letra que ocupa esa posición en la clave.
        ciphertext += key[number]

    # Devolvemos el mensaje cifrado.
    return ciphertext


def decrypt(ciphertext: str, key: str) -> str:
    # Comprobamos que la clave sea válida.
    validate_key(key)

    # Normalizamos el texto cifrado para trabajar solo con A-Z.
    normalized = to_letters(to_numbers(ciphertext))

    # Creamos el texto donde guardaremos el mensaje recuperado.
    plaintext = ""

    # Recorremos las letras cifradas.
    for character in normalized:
        # Buscamos en qué posición de la clave está la letra cifrada.
        position = key.index(character)

        # Recuperamos la letra original situada ahí en el alfabeto.
        plaintext += ALPHABET[position]

    # Devolvemos el mensaje descifrado.
    return plaintext


def key_from_keyword(keyword: str) -> str:
    # Normalizamos la palabra clave: mayúsculas y solo letras A-Z.
    normalized = to_letters(to_numbers(keyword))

    # Empezamos con una clave vacía.
    key = ""

    # Recorremos las letras de la palabra clave.
    for character in normalized:
        # Añadimos cada letra solo la primera vez que aparece.
        if character not in key:
            key += character

    # Recorremos el alfabeto para completar la clave.
    for character in ALPHABET:
        # Añadimos las letras que todavía no están en la clave.
        if character not in key:
            key += character

    # Devolvemos la permutación completa de 26 letras.
    return key
