# Counter permite contar cuántas veces aparece cada letra.
from collections import Counter

# Importamos el descifrado César y le damos un nombre más descriptivo.
from caesar import decrypt as caesar_decrypt

# Importamos la función que devuelve las frecuencias de cada idioma.
from frequencies import get_frequencies

# Importamos las conversiones para normalizar el texto.
from basics import to_numbers, to_letters


def chi_squared(text: str, table: dict[str, float]) -> float:
    # Normalizamos el texto: mayúsculas y solo letras A-Z.
    normalized = to_letters(to_numbers(text))

    # No podemos calcular frecuencias de un texto sin letras.
    if len(normalized) == 0:
        raise ValueError("No se puede puntuar un texto sin letras A-Z")

    # Comprobamos que la tabla contenga las 26 letras.
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if set(table.keys()) != set(alphabet):
        raise ValueError("La tabla debe contener exactamente las letras A-Z")

    # Contamos cuántas veces aparece cada letra en el texto.
    counts = Counter(normalized)

    # Guardaremos aquí la puntuación total.
    score = 0.0

    # Longitud del texto normalizado.
    length = len(normalized)

    # Comparamos cada letra con su frecuencia esperada.
    for letter in alphabet:
        # Frecuencia esperada de esta letra en el idioma.
        expected_frequency = table[letter]

        # Todas las frecuencias esperadas deben ser positivas.
        if expected_frequency <= 0:
            raise ValueError(
                f"La frecuencia esperada de {letter} debe ser positiva"
            )

        # Convertimos el número de apariciones en una proporción.
        observed_frequency = counts[letter] / length

        # Añadimos la contribución de esta letra al chi-cuadrado.
        score += (
            (observed_frequency - expected_frequency) ** 2
            / expected_frequency
        )

    # La puntuación ya está normalizada por la longitud,
    # porque trabajamos con proporciones y no con conteos brutos.
    return score


def break_caesar(
    ciphertext: str,
    language: str = "en"
) -> tuple[int, str]:
    # Obtenemos la tabla de frecuencias del idioma solicitado.
    table = get_frequencies(language)

    # Normalizamos el mensaje cifrado.
    normalized = to_letters(to_numbers(ciphertext))

    # Sin letras no podemos averiguar ninguna clave.
    if len(normalized) == 0:
        raise ValueError("El texto cifrado debe contener alguna letra A-Z")

    # Inicializamos la mejor clave y el mejor texto.
    best_key = 0
    best_plaintext = ""

    # Empezamos con una puntuación infinita.
    # Cualquier puntuación real será menor.
    best_score = float("inf")

    # Probamos las 26 claves posibles de César.
    for key in range(26):
        # Desciframos el texto suponiendo que esta es la clave.
        candidate = caesar_decrypt(normalized, key)

        # Calculamos cuánto se parece al idioma.
        score = chi_squared(candidate, table)

        # Si mejora la puntuación anterior, guardamos este resultado.
        if score < best_score:
            best_score = score
            best_key = key
            best_plaintext = candidate

    # Devolvemos la clave encontrada y el mensaje descifrado.
    return best_key, best_plaintext
