import unittest

from railfence import encrypt, decrypt


class TestRailFence(unittest.TestCase):

    def test_published_values(self):
        self.assertEqual(
            encrypt("MYSECRETMESSAGE", 2),
            "MSCEMSAEYERTESG"
        )

        self.assertEqual(
            encrypt("MYSECRETMESSAGE", 3),
            "MCMAYERTESGSESE"
        )

        self.assertEqual(
            encrypt("MYSECRETMESSAGE", 4),
            "MEAYRTSGSCMSEEE"
        )

    def test_round_trip(self):
        messages = [
            "MYSECRETMESSAGE",
            "THE INDEX OF COINCIDENCE",
            "Cryptography is interesting!",
            "",
            "A",
        ]

        for message in messages:
            for rails in range(2, 8):
                ciphertext = encrypt(message, rails)
                plaintext = decrypt(ciphertext, rails)

                expected = "".join(
                    character
                    for character in message.upper()
                    if "A" <= character <= "Z"
                )

                self.assertEqual(plaintext, expected)

    def test_normalization(self):
        self.assertEqual(
            encrypt("My secret message!", 3),
            encrypt("MYSECRETMESSAGE", 3)
        )

    def test_empty_input(self):
        self.assertEqual(encrypt("", 3), "")
        self.assertEqual(decrypt("", 3), "")

    def test_single_character(self):
        self.assertEqual(encrypt("A", 3), "A")
        self.assertEqual(decrypt("A", 3), "A")

    def test_invalid_rails(self):
        with self.assertRaises(ValueError):
            encrypt("MESSAGE", 1)

        with self.assertRaises(ValueError):
            decrypt("MESSAGE", 0)

        with self.assertRaises(ValueError):
            encrypt("MESSAGE", 2.5)


if __name__ == "__main__":
    unittest.main()

    