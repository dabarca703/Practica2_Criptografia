# columnar.py

from basics import to_numbers, to_letters


def _normalize_keyword(keyword: str) -> str:
    """Normaliza y valida una palabra clave."""
    normalized = to_letters(to_numbers(keyword))

    if len(normalized) == 0:
        raise ValueError("La palabra clave debe contener alguna letra A-Z")

    return normalized


def key_order(keyword: str) -> list[int]:
    """
    Numera las letras de la clave en orden alfabético.

    Los empates se resuelven de izquierda a derecha.
    """
    normalized = _normalize_keyword(keyword)

    # Creamos una lista con las posiciones de la palabra:
    # [0, 1, 2, ..., longitud - 1]
    positions = list(range(len(normalized)))

    # Ordenamos las posiciones usando:
    # 1. La letra situada en esa posición.
    # 2. La propia posición para resolver letras repetidas.
    sorted_positions = sorted(
        positions,
        key=lambda position: (normalized[position], position)
    )

    # Aquí guardaremos el número asignado a cada columna.
    order = [0] * len(normalized)

    # La primera letra alfabéticamente recibe 1,
    # la segunda recibe 2, etc.
    for number, position in enumerate(sorted_positions, start=1):
        order[position] = number

    return order

def _normalize_pad(pad: str) -> str:
    """Comprueba que el carácter de relleno sea una única letra A-Z."""
    normalized = to_letters(to_numbers(pad))

    if len(normalized) != 1:
        raise ValueError(
            "El carácter de relleno debe ser una única letra A-Z"
        )

    return normalized

def encrypt(
    plaintext: str,
    keyword: str,
    pad: str = "X"
) -> str:
    """Cifra un texto mediante transposición columnar."""
    normalized = to_letters(to_numbers(plaintext))
    normalized_keyword = _normalize_keyword(keyword)
    normalized_pad = _normalize_pad(pad)

    # El número de columnas coincide con la longitud de la clave.
    number_of_columns = len(normalized_keyword)

    # Calculamos cuántas letras faltan para completar la última fila.
    padding_needed = (
        -len(normalized)
    ) % number_of_columns

    # Añadimos el padding necesario.
    padded_plaintext = (
        normalized
        + normalized_pad * padding_needed
    )

    # Calculamos la numeración de las columnas.
    order = key_order(normalized_keyword)

    # Obtenemos las posiciones de las columnas en el orden
    # en el que deben leerse.
    ordered_columns = sorted(
        range(number_of_columns),
        key=lambda column: order[column]
    )

    ciphertext = ""

    # Leemos primero la columna con número 1,
    # después la columna con número 2, etc.
    for column in ordered_columns:
        for position in range(
            column,
            len(padded_plaintext),
            number_of_columns
        ):
            ciphertext += padded_plaintext[position]

    return ciphertext

def decrypt(ciphertext: str, keyword: str) -> str:
    """
    Descifra un texto cifrado mediante transposición columnar.

    El resultado conserva los caracteres de relleno.
    """
    normalized = to_letters(to_numbers(ciphertext))
    normalized_keyword = _normalize_keyword(keyword)

    number_of_columns = len(normalized_keyword)

    # Un criptograma columnar válido debe contener filas completas.
    if len(normalized) % number_of_columns != 0:
        raise ValueError(
            "La longitud del criptograma debe ser múltiplo "
            "de la longitud de la clave"
        )

    # Si el criptograma está vacío, el resultado también lo está.
    if len(normalized) == 0:
        return ""

    number_of_rows = len(normalized) // number_of_columns

    # Calculamos el orden numérico de la clave.
    order = key_order(normalized_keyword)

    # Posiciones originales de las columnas, ordenadas
    # según los números 1, 2, 3...
    ordered_columns = sorted(
        range(number_of_columns),
        key=lambda column: order[column]
    )

    # Aquí colocaremos cada columna en su posición original.
    columns = [""] * number_of_columns

    # Recorremos el criptograma tomando un fragmento
    # de number_of_rows letras para cada columna.
    start = 0

    for column in ordered_columns:
        end = start + number_of_rows
        columns[column] = normalized[start:end]
        start = end

    # Reconstruimos el texto leyendo la tabla por filas.
    plaintext = ""

    for row in range(number_of_rows):
        for column in range(number_of_columns):
            plaintext += columns[column][row]

    return plaintext

import math


def encrypt_double(
    plaintext: str,
    kw1: str,
    kw2: str,
    pad: str = "X"
) -> str:
    """Aplica dos transposiciones columnares consecutivas."""
    normalized = to_letters(to_numbers(plaintext))

    # key_order valida las claves y su longitud indica el número de columnas.
    columns1 = len(key_order(kw1))
    columns2 = len(key_order(kw2))

    # Completamos hasta una longitud divisible por ambas claves.
    block_size = math.lcm(columns1, columns2)
    padding_needed = (-len(normalized)) % block_size
    padded = normalized + _normalize_pad(pad) * padding_needed

    # La salida de la primera pasada es la entrada de la segunda.
    first_pass = encrypt(padded, kw1, pad)
    return encrypt(first_pass, kw2, pad)


def decrypt_double(ciphertext: str, kw1: str, kw2: str) -> str:
    """Deshace las dos transposiciones en orden inverso."""
    # Primero se deshace la última pasada; después, la primera.
    after_second_pass = decrypt(ciphertext, kw2)
    return decrypt(after_second_pass, kw1)






