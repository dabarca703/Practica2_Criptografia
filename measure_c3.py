import random
import string

from basics import to_numbers, to_letters
from break_columnar import attack
from columnar import encrypt


COLUMN_COUNTS = [4, 5, 6, 7]
PLAINTEXT_LENGTHS = [60, 120, 200]
TRIALS = 100
SEED = 2027


def random_chunk(text: str, length: int) -> str:
    start = random.randint(0, len(text) - length)
    return text[start:start + length]


def main():
    random.seed(SEED)

    with open("data/reference_en.txt", encoding="utf-8") as file:
        reference = to_letters(to_numbers(file.read()))

    results = {
        (columns, length): 0
        for columns in COLUMN_COUNTS
        for length in PLAINTEXT_LENGTHS
    }

    total_cases = len(COLUMN_COUNTS) * len(PLAINTEXT_LENGTHS) * TRIALS
    completed = 0

    for columns in COLUMN_COUNTS:
        for length in PLAINTEXT_LENGTHS:
            for _ in range(TRIALS):
                plaintext = random_chunk(reference, length)

                # Letras sin repetir generan un orden de columnas
                # aleatorio y sin empates.
                keyword = "".join(
                    random.sample(string.ascii_uppercase, columns)
                )

                ciphertext = encrypt(plaintext, keyword)
                expected = plaintext + "X" * ((-len(plaintext)) % columns)

                _, recovered = attack(ciphertext, n_cols=columns)

                if recovered == expected:
                    results[(columns, length)] += 1

                completed += 1

            print(
                f"Completado: {columns} columnas, "
                f"{length} letras de texto original "
                f"({completed}/{total_cases})"
            )

    print("\nPorcentaje de textos recuperados exactamente")
    print("Columnas | " + " | ".join(map(str, PLAINTEXT_LENGTHS)))

    for columns in COLUMN_COUNTS:
        row = [
            f"{100 * results[(columns, length)] / TRIALS:.1f}%"
            for length in PLAINTEXT_LENGTHS
        ]
        print(f"{columns:8} | " + " | ".join(row))


if __name__ == "__main__":
    main()

                