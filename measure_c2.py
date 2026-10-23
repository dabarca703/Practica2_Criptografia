import random

from basics import to_numbers, to_letters
from break_vigenere import attack
from vigenere import encrypt


KEY_LENGTHS = [3, 5, 7, 9]
TEXT_LENGTHS = [100, 150, 200, 300, 400]
TRIALS = 100
SEED = 2026


def random_chunk(text: str, length: int) -> str:
    start = random.randint(0, len(text) - length)
    return text[start:start + length]


def random_key(length: int) -> str:
    return "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(length))


def main():
    random.seed(SEED)

    with open("data/reference_en.txt", encoding="utf-8") as file:
        reference = to_letters(to_numbers(file.read()))

    if len(reference) < max(TEXT_LENGTHS):
        raise ValueError("El texto de referencia es demasiado corto")

    # Guardamos aciertos por longitud de clave y longitud del criptograma.
    correct_key = {
        (key_length, text_length): 0
        for key_length in KEY_LENGTHS
        for text_length in TEXT_LENGTHS
    }
    correct_length = correct_key.copy()

    total_cases = len(KEY_LENGTHS) * len(TEXT_LENGTHS) * TRIALS
    case_number = 0

    for key_length in KEY_LENGTHS:
        for text_length in TEXT_LENGTHS:
            for _ in range(TRIALS):
                plaintext = random_chunk(reference, text_length)
                key = random_key(key_length)
                ciphertext = encrypt(plaintext, key)

                recovered_key, _ = attack(ciphertext)
                case_number += 1

                if len(recovered_key) == key_length:
                    correct_length[(key_length, text_length)] += 1

                if recovered_key == key:
                    correct_key[(key_length, text_length)] += 1

            print(
                f"Completado: clave {key_length}, "
                f"texto {text_length} "
                f"({case_number}/{total_cases})"
            )

    print("\nPorcentaje de claves completas recuperadas")
    print("Clave\\Texto | " + " | ".join(map(str, TEXT_LENGTHS)))

    for key_length in KEY_LENGTHS:
        row = [
            f"{100 * correct_key[(key_length, n)] / TRIALS:.1f}%"
            for n in TEXT_LENGTHS
        ]
        print(f"{key_length:11} | " + " | ".join(row))

    print("\nPorcentaje de longitudes de clave acertadas")
    print("Clave\\Texto | " + " | ".join(map(str, TEXT_LENGTHS)))

    for key_length in KEY_LENGTHS:
        row = [
            f"{100 * correct_length[(key_length, n)] / TRIALS:.1f}%"
            for n in TEXT_LENGTHS
        ]
        print(f"{key_length:11} | " + " | ".join(row))


if __name__ == "__main__":
    main()

    