from basics import to_numbers, to_letters
from break_caesar import chi_squared
from frequencies import get_frequencies



def index_of_coincidence(text: str) -> float:
    """Calcula el índice de coincidencia de las letras A-Z."""
    normalized = to_letters(to_numbers(text))
    n = len(normalized)

    # Con menos de dos letras, n * (n - 1) sería cero.
    if n < 2:
        return 0.0

    counts = [0] * 26

    for letter in normalized:
        index = ord(letter) - ord("A")
        counts[index] += 1

    numerator = sum(
        count * (count - 1)
        for count in counts
    )

    denominator = n * (n - 1)

    return numerator / denominator

# Umbral obtenido con las mediciones de measure_b2.py.
CLASSIFIER_THRESHOLD = 2.551736


def classify(ciphertext: str, language: str = "en") -> str:
    """Clasifica el texto como transposición o sustitución."""
    normalized = to_letters(to_numbers(ciphertext))

    if len(normalized) == 0:
        raise ValueError("El texto debe contener alguna letra A-Z")

    table = get_frequencies(language)
    score = chi_squared(normalized, table)

    if score <= CLASSIFIER_THRESHOLD:
        return "transposition"

    return "substitution"

