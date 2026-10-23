import unittest

from keylength import coset_ic, find_key_length
from vigenere import encrypt


class TestKeyLength(unittest.TestCase):

    def test_coset_ic_invalid_m(self):
        with self.assertRaises(ValueError):
            coset_ic("ABCDEF", 0)

    def test_find_key_length_invalid_input(self):
        with self.assertRaises(ValueError):
            find_key_length("123 !!!")

    def test_coset_ic_returns_float(self):
        result = coset_ic("THEINDEXOFCOINCIDENCE", 3)
        self.assertIsInstance(result, float)

    def test_finds_key_length_on_long_text(self):
        with open("data/reference_en.txt", encoding="utf-8") as file:
            text = file.read()

        ciphertext = encrypt(text, "LEMON")
        self.assertEqual(find_key_length(ciphertext, max_m=16), 5)


if __name__ == "__main__":
    unittest.main()

    