# Importamos el descifrado afín y la lista de claves válidas.
from affine import decrypt as affine_decrypt, valid_keys

# Reutilizamos la puntuación estadística del ataque a César.
from break_caesar import chi_squared

# Importamos las tablas de frecuencias.
from frequencies import get_frequencies

# Importamos las conversiones para normalizar el texto.
from basics import to_numbers, to_letters


def break_affine(
    ciphertext: str,
    language: str = "en"
) -> tuple[tuple[int, int], str]:
    # Obtenemos la tabla de frecuencias del idioma solicitado.
    table = get_frequencies(language)

    # Normalizamos el criptograma.
    normalized = to_letters(to_numbers(ciphertext))

    # No podemos atacar un texto que no contiene letras.
    if len(normalized) == 0:
        raise ValueError("El texto cifrado debe contener alguna letra A-Z")

    # Inicializamos la mejor clave.
    best_key = (1, 0)

    # Inicializamos el mejor texto recuperado.
    best_plaintext = ""

    # Empezamos con una puntuación infinita.
    best_score = float("inf")

    # Probamos las 312 parejas de claves válidas.
    for a, b in valid_keys():
        # Desciframos suponiendo que esta es la clave.
        candidate = affine_decrypt(normalized, a, b)

        # Medimos cuánto se parece el resultado al idioma.
        score = chi_squared(candidate, table)

        # Si esta clave produce un texto mejor, la guardamos.
        if score < best_score:
            best_score = score
            best_key = (a, b)
            best_plaintext = candidate

    # Devolvemos la pareja (a, b) y el mensaje recuperado.
    return best_key, best_plaintext

