from collections import Counter
from itertools import permutations
from math import log
from pathlib import Path
from functools import lru_cache

from basics import to_numbers, to_letters


def _normalize(text: str) -> str:
    return to_letters(to_numbers(text))


@lru_cache(maxsize=2)
def _load_bigram_scores(language: str) -> list[float]:
    if language not in {"en", "es"}:
        raise ValueError("language debe ser 'en' o 'es'")

    corpus_path = Path(__file__).parent / "data" / f"reference_{language}.txt"
    corpus = _normalize(corpus_path.read_text(encoding="utf-8"))

    if len(corpus) < 2:
        raise ValueError("El corpus debe contener al menos dos letras")

    counts = Counter(
        corpus[i:i + 2]
        for i in range(len(corpus) - 1)
    )
    total = len(corpus) - 1

    alphabet_size = 26
    denominator = total + alphabet_size ** 2

    return [
        log((counts[first + second] + 1) / denominator)
        for first in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for second in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ]


def _decrypt_order(ciphertext: str, order: tuple[int, ...]) -> str:
    number_of_columns = len(order)
    number_of_rows = len(ciphertext) // number_of_columns
    columns = [""] * number_of_columns

    start = 0
    for column in order:
        columns[column] = ciphertext[start:start + number_of_rows]
        start += number_of_rows

    return "".join(
        columns[column][row]
        for row in range(number_of_rows)
        for column in range(number_of_columns)
    )


def _bigram_score(text: str, scores: list[float]) -> float:
    return sum(
        scores[(ord(first) - 65) * 26 + (ord(second) - 65)]
        for first, second in zip(text, text[1:])
    )


def attack(
    ciphertext: str,
    n_cols: int,
    language: str = "en"
) -> tuple[tuple[int, ...], str]:
    """Prueba todos los órdenes y devuelve (orden de columnas, texto candidato)."""
    if (
        not isinstance(n_cols, int)
        or isinstance(n_cols, bool)
        or n_cols < 2
    ):
        raise ValueError("n_cols debe ser un entero de al menos 2")

    normalized = _normalize(ciphertext)

    if not normalized:
        raise ValueError("El texto cifrado debe contener letras A-Z")

    if len(normalized) < n_cols:
        raise ValueError("El texto es más corto que el número de columnas")

    if len(normalized) % n_cols != 0:
        raise ValueError(
            "La longitud del texto cifrado debe ser múltiplo de n_cols"
        )

    scores = _load_bigram_scores(language)
    best_order = None
    best_plaintext = ""
    best_score = float("-inf")

    for order in permutations(range(n_cols)):
        candidate = _decrypt_order(normalized, order)
        score = _bigram_score(candidate, scores)

        if score > best_score:
            best_score = score
            best_order = order
            best_plaintext = candidate

    return best_order, best_plaintext



