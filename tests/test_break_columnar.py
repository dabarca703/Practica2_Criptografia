import unittest

from basics import to_numbers, to_letters
from break_columnar import attack
from columnar import encrypt


class TestBreakColumnar(unittest.TestCase):

    def test_recovers_plaintext(self):
        with open("data/reference_en.txt", encoding="utf-8") as file:
            plaintext = to_letters(to_numbers(file.read()))

        plaintext = plaintext[:400]
        expected = plaintext + "X" * ((-len(plaintext)) % 6)
        ciphertext = encrypt(plaintext, "CIPHER")

        order, recovered = attack(ciphertext, n_cols=6)

        self.assertEqual(recovered, expected)
        self.assertEqual(order, (0, 4, 3, 1, 2, 5))

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            attack("", n_cols=4)

        with self.assertRaises(ValueError):
            attack("ABC", n_cols=4)

        with self.assertRaises(ValueError):
            attack("ABCDEFG", n_cols=3)


    def test_recovers_20_generated_ciphertexts(self):
        import random
        import string

        generator = random.Random(2027)

        with open("data/reference_en.txt", encoding="utf-8") as file:
            reference = to_letters(to_numbers(file.read()))

        for _ in range(20):
            start = generator.randint(0, len(reference) - 120)
            plaintext = reference[start:start + 120]
            keyword = "".join(generator.sample(string.ascii_uppercase, 7))
            ciphertext = encrypt(plaintext, keyword)

            _, recovered = attack(ciphertext, n_cols=7)

            expected = plaintext + "X" * ((-len(plaintext)) % 7)
            self.assertEqual(recovered, expected)

if __name__ == "__main__":
    unittest.main()






