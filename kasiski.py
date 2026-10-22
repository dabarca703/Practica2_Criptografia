from collections import defaultdict

from basics import to_numbers, to_letters


def _normalize(text: str) -> str:
    return to_letters(to_numbers(text))


def repeats(ciphertext: str, min_len: int = 3) -> dict[str, list[int]]:
    """Devuelve las secuencias repetidas y las posiciones donde empiezan."""
    if not isinstance(min_len, int) or isinstance(min_len, bool) or min_len < 1:
        raise ValueError("min_len debe ser un entero positivo")

    text = _normalize(ciphertext)
    found = {}

    # Probamos secuencias desde min_len hasta la longitud del texto.
    for length in range(min_len, len(text) + 1):
        positions_by_sequence = defaultdict(list)

        for start in range(len(text) - length + 1):
            sequence = text[start:start + length]
            positions_by_sequence[sequence].append(start)

        # Solo guardamos las secuencias que aparecen más de una vez.
        for sequence, positions in positions_by_sequence.items():
            if len(positions) > 1:
                found[sequence] = positions

    return found


def _is_contained_repeat(
    sequence: str,
    positions: list[int],
    all_repeats: dict[str, list[int]]
) -> bool:
    """Comprueba si la repetición ya está dentro de otra más larga."""
    for longer, longer_positions in all_repeats.items():
        if len(longer) <= len(sequence):
            continue

        offset = longer.find(sequence)

        while offset != -1:
            shifted_positions = sorted(
                start + offset for start in longer_positions
            )

            if shifted_positions == sorted(positions):
                return True

            offset = longer.find(sequence, offset + 1)

    return False


def distances(ciphertext: str, min_len: int = 3) -> list[int]:
    """Devuelve las distancias distintas entre repeticiones máximas."""
    repeated = repeats(ciphertext, min_len)
    unique_distances = set()

    for sequence, positions in repeated.items():
        # Ignoramos las repeticiones que ya aparecen dentro
        # de una secuencia repetida más larga en las mismas posiciones.
        if _is_contained_repeat(sequence, positions, repeated):
            continue

        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                unique_distances.add(positions[j] - positions[i])

    return sorted(unique_distances)


def factor_tally(
    ciphertext: str,
    max_factor: int = 20
) -> dict[int, int]:
    """Cuenta cuántas distancias son divisibles por cada factor posible."""
    if (
        not isinstance(max_factor, int)
        or isinstance(max_factor, bool)
        or max_factor < 2
    ):
        raise ValueError("max_factor debe ser un entero de al menos 2")

    observed_distances = distances(ciphertext)

    return {
        factor: sum(
            distance % factor == 0
            for distance in observed_distances
        )
        for factor in range(2, max_factor + 1)
    }

