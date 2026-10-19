import random
import string
from pathlib import Path

from break_caesar import chi_squared
from basics import to_numbers, to_letters
from columnar import encrypt as columnar_encrypt
from frequencies import get_frequencies
from monoalpha import encrypt as monoalpha_encrypt


LENGTHS = [60, 120, 250, 400]
SAMPLES_PER_CLASS = 200
RANDOM_SEED = 42
ALPHABET = string.ascii_uppercase


def load_reference_text() -> str:
    path = Path("data/reference_en.txt")
    text = path.read_text(encoding="utf-8")
    normalized = to_letters(to_numbers(text))

    if len(normalized) < 700:
        raise ValueError(
            f"El corpus tiene solo {len(normalized)} letras; hacen falta 700."
        )

    return normalized


def random_chunk(text: str, length: int) -> str:
    start = random.randint(0, len(text) - length)
    return text[start:start + length]


def random_keyword() -> str:
    size = random.randint(2, 10)
    return "".join(random.choices(ALPHABET, k=size))


def random_monoalphabetic_key() -> str:
    letters = list(ALPHABET)
    random.shuffle(letters)
    return "".join(letters)


def choose_threshold(transposition_scores, substitution_scores) -> float:
    """Elige el umbral que minimiza los errores en las muestras de calibración."""
    values = sorted(set(transposition_scores + substitution_scores))

    candidates = [
        (left + right) / 2
        for left, right in zip(values, values[1:])
    ]

    best_threshold = candidates[0]
    best_errors = float("inf")

    for threshold in candidates:
        # Puntuación baja -> transposición.
        errors = sum(
            score > threshold for score in transposition_scores
        )
        # Puntuación alta -> sustitución.
        errors += sum(
            score <= threshold for score in substitution_scores
        )

        if errors < best_errors:
            best_errors = errors
            best_threshold = threshold

    return best_threshold


def main():
    random.seed(RANDOM_SEED)

    reference = load_reference_text()
    expected = get_frequencies("en")
    random_pad_letters = list(expected.keys())
    random_pad_weights = list(expected.values())

    results = {
        "X": {"transposition": [], "substitution": []},
        "random": {"transposition": [], "substitution": []},
    }

    for length in LENGTHS:
        for _ in range(SAMPLES_PER_CLASS):
            plaintext = random_chunk(reference, length)

            # Transposición columnar con relleno constante X.
            keyword = random_keyword()
            ciphertext = columnar_encrypt(plaintext, keyword, pad="X")
            score = chi_squared(ciphertext, expected)
            results["X"]["transposition"].append((length, score))

            # Transposición columnar con relleno elegido según
            # las frecuencias de las letras inglesas.
            random_pad = random.choices(
                random_pad_letters,
                weights=random_pad_weights,
                k=1
            )[0]
            ciphertext = columnar_encrypt(
                plaintext,
                keyword,
                pad=random_pad
            )
            score = chi_squared(ciphertext, expected)
            results["random"]["transposition"].append((length, score))

            # Sustitución monoalfabética.
            mono_key = random_monoalphabetic_key()
            ciphertext = monoalpha_encrypt(plaintext, mono_key)
            score = chi_squared(ciphertext, expected)

            # Usamos las mismas muestras de sustitución para comparar
            # los dos tipos de relleno.
            results["X"]["substitution"].append((length, score))
            results["random"]["substitution"].append((length, score))

    # 50 muestras por clase sirven para elegir el umbral.
    # Las 150 restantes por clase sirven para medir los errores.
    for padding_type in ["X", "random"]:
        transposition = results[padding_type]["transposition"]
        substitution = results[padding_type]["substitution"]

        train_trans = [score for _, score in transposition[:50]]
        train_sub = [score for _, score in substitution[:50]]

        threshold = choose_threshold(train_trans, train_sub)

        print(f"\nRelleno: {padding_type}")
        print(f"Umbral elegido con las primeras 50 muestras: {threshold:.6f}")
        print("Longitud | Error transposición | Error sustitución | Error total")

        total_errors = 0
        total_tests = 0

        for length in LENGTHS:
            test_trans = [
                score for sample_length, score in transposition[50:]
                if sample_length == length
            ]
            test_sub = [
                score for sample_length, score in substitution[50:]
                if sample_length == length
            ]

            errors_trans = sum(score > threshold for score in test_trans)
            errors_sub = sum(score <= threshold for score in test_sub)
            errors = errors_trans + errors_sub
            tests = len(test_trans) + len(test_sub)

            total_errors += errors
            total_tests += tests

            print(
                f"{length:8} | "
                f"{errors_trans / len(test_trans):18.1%} | "
                f"{errors_sub / len(test_sub):16.1%} | "
                f"{errors / tests:11.1%}"
            )

        print(f"Error total de evaluación: {total_errors / total_tests:.1%}")


if __name__ == "__main__":
    main()
    