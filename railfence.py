# railfence.py

from basics import to_numbers, to_letters


def _validate_rails(rails: int) -> None:
    """Comprueba que el número de raíles sea válido."""
    if not isinstance(rails, int) or isinstance(rails, bool):
        raise ValueError("El número de raíles debe ser un entero")

    if rails < 2:
        raise ValueError("El número de raíles debe ser al menos 2")


def _rail_pattern(length: int, rails: int) -> list[int]:
    """
    Devuelve el raíl correspondiente a cada posición del mensaje.

    Por ejemplo, para 3 raíles:
    0, 1, 2, 1, 0, 1, 2, 1...
    """
    pattern = []

    current_rail = 0
    direction = 1

    for _ in range(length):
        pattern.append(current_rail)

        # Al llegar al primer raíl, comenzamos a bajar.
        if current_rail == 0:
            direction = 1

        # Al llegar al último raíl, comenzamos a subir.
        elif current_rail == rails - 1:
            direction = -1

        current_rail += direction

    return pattern


def encrypt(plaintext: str, rails: int) -> str:
    """Cifra un texto utilizando el cifrado Rail Fence."""
    _validate_rails(rails)

    # Reutilizamos la normalización de la Práctica 1:
    # convertimos a mayúsculas y eliminamos todo lo que no sea A-Z.
    normalized = to_letters(to_numbers(plaintext))

    # Creamos una cadena vacía para cada raíl.
    rows = [""] * rails

    # Calculamos el recorrido en zigzag.
    pattern = _rail_pattern(len(normalized), rails)

    # Colocamos cada letra en el raíl correspondiente.
    for character, rail in zip(normalized, pattern):
        rows[rail] += character

    # Leemos los raíles de arriba abajo.
    return "".join(rows)


def decrypt(ciphertext: str, rails: int) -> str:
    """Descifra un texto cifrado mediante Rail Fence."""
    _validate_rails(rails)

    normalized = to_letters(to_numbers(ciphertext))

    # Calculamos qué raíl corresponde a cada posición
    # del texto original.
    pattern = _rail_pattern(len(normalized), rails)

    # Contamos cuántas letras pertenecen a cada raíl.
    rail_lengths = []

    for rail in range(rails):
        rail_lengths.append(pattern.count(rail))

    # Separamos el criptograma en los fragmentos que corresponden
    # a cada raíl.
    rail_contents = []
    start = 0

    for length in rail_lengths:
        end = start + length
        rail_contents.append(normalized[start:end])
        start = end

    # Guardamos qué letra hemos utilizado ya de cada raíl.
    rail_positions = [0] * rails

    # Reconstruimos el recorrido original en zigzag.
    plaintext = ""

    for rail in pattern:
        position = rail_positions[rail]
        plaintext += rail_contents[rail][position]
        rail_positions[rail] += 1

    return plaintext

