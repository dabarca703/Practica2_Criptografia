from basics import to_numbers, to_letters
from frequencies import get_frequencies


def _normalize(text: str) -> str:
    return to_letters(to_numbers(text))


def _index_of_coincidence(text: str) -> float:
    """Calcula el índice de coincidencia de un texto ya normalizado."""
    n = len(text)

    if n < 2:
        return 0.0

    counts = [0] * 26

    for letter in text:
        counts[ord(letter) - ord("A")] += 1

    numerator = sum(count * (count - 1) for count in counts)
    return numerator / (n * (n - 1))


def coset_ic(ciphertext: str, m: int) -> float:
    """Devuelve el IC medio de los m grupos de letras del texto."""
    if not isinstance(m, int) or isinstance(m, bool) or m < 1:
        raise ValueError("m debe ser un entero positivo")

    text = _normalize(ciphertext)

    if not text:
        return 0.0

    cosets = [text[offset::m] for offset in range(m)]
    return sum(_index_of_coincidence(coset) for coset in cosets) / m


def find_key_length(
    ciphertext: str,
    max_m: int = 16,
    language: str = "en"
) -> int:
    """Estima la longitud de clave con el menor IC claramente alto."""
    if (
        not isinstance(max_m, int)
        or isinstance(max_m, bool)
        or max_m < 1
    ):
        raise ValueError("max_m debe ser un entero positivo")

    text = _normalize(ciphertext)

    if not text:
        raise ValueError("El texto debe contener letras A-Z")

    # IC esperado de letras uniformemente aleatorias.
    random_baseline = 1 / 26

    # IC esperado según las frecuencias del idioma elegido.
    frequencies = get_frequencies(language)

    language_ic = sum(
        frequency ** 2 for frequency in frequencies.values()
    )

    # Consideramos "claramente alto" un valor situado por encima
    # del punto medio entre el baseline aleatorio y el IC del idioma.
    threshold = (random_baseline + language_ic) / 2

    values = {
        m: coset_ic(text, m)
        for m in range(1, min(max_m, len(text)) + 1)
    }

    # Cada múltiplo de la longitud verdadera también puede dar un IC alto.
    # Por eso devolvemos el primer m que supera el umbral.
    for m, value in values.items():
        if value > threshold:
            return m

    # Si ningún valor supera el umbral, devolvemos el m con el IC mayor.
    return max(values, key=values.get)
