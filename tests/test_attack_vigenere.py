import unittest
import random

from basics import to_numbers, to_letters
from break_vigenere import attack
from vigenere import encrypt


class TestAutomaticVigenereAttack(unittest.TestCase):

    def test_recovers_key_and_plaintext(self):
        with open("data/reference_en.txt", encoding="utf-8") as file:
            plaintext = to_letters(to_numbers(file.read()))

        plaintext = plaintext[:10000]
        ciphertext = encrypt(plaintext, "LEMON")

        key, recovered_plaintext = attack(ciphertext)

        self.assertEqual(key, "LEMON")
        self.assertEqual(recovered_plaintext, plaintext)

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            attack("123 !!!")

    def test_recovers_20_generated_ciphertexts(self):
        generator = random.Random(2026)

        with open("data/reference_en.txt", encoding="utf-8") as file:
            reference = to_letters(to_numbers(file.read()))

        for _ in range(20):
            start = generator.randint(0, len(reference) - 400)
            plaintext = reference[start:start + 400]

            key = "".join(
                generator.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                for _ in range(7)
            )

            ciphertext = encrypt(plaintext, key)
            recovered_key, recovered_plaintext = attack(ciphertext)

            self.assertEqual(recovered_key, key)
            self.assertEqual(recovered_plaintext, plaintext)


if __name__ == "__main__":
    unittest.main()

    

            





