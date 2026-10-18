from basics import to_numbers, to_letters


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

