import unittest

from columnar import key_order, encrypt, decrypt


class TestColumnar(unittest.TestCase):

    def test_key_order(self):
        self.assertEqual(key_order("CIPHER"), [1, 4, 5, 3, 2, 6])
        self.assertEqual(key_order("ROTOR"), [3, 1, 5, 2, 4])

    def test_published_encryption(self):
        self.assertEqual(
            encrypt("MYSECRETMESSAGE", "CIPHER"),
            "MEACSXEEXYTGSMERSX"
        )

        self.assertEqual(
            encrypt("THE INDEX OF COINCIDENCE", "KASISKI"),
            "HOIICEENETXCDICEFDNON"
        )

    def test_custom_padding(self):
        self.assertEqual(
        encrypt("MYSECRETMESSAGE", "CIPHER", pad="Q"),
        "MEACSQEEQYTGSMERSQ"
    )

    def test_decryption(self):
        self.assertEqual(
            decrypt("MEACSXEEXYTGSMERSX", "CIPHER"),
            "MYSECRETMESSAGEXXX"
        )

        self.assertEqual(
            decrypt("HOIICEENETXCDICEFDNON", "KASISKI"),
            "THEINDEXOFCOINCIDENCE"
        )

    def test_round_trip(self):
        messages = [
            "MYSECRETMESSAGE",
            "THE INDEX OF COINCIDENCE",
            "Cryptography!",
            "",
            "A",
        ]

        for message in messages:
            for keyword in ["KEY", "CIPHER", "ROTOR"]:
                ciphertext = encrypt(message, keyword)
                expected = "".join(
                    character
                    for character in message.upper()
                    if "A" <= character <= "Z"
                )

                # El cifrado completa la tabla con X si hace falta.
                expected += "X" * (
                    (-len(expected)) % len(keyword)
                )

                self.assertEqual(decrypt(ciphertext, keyword), expected)

    def test_invalid_keyword_and_padding(self):
        with self.assertRaises(ValueError):
            key_order("123!")

        with self.assertRaises(ValueError):
            encrypt("MESSAGE", "KEY", pad="XX")

    def test_invalid_ciphertext_length(self):
        with self.assertRaises(ValueError):
            decrypt("ABCDE", "KEY")


if __name__ == "__main__":
    unittest.main()

