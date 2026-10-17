import unittest

from columnar import encrypt_double, decrypt_double


class TestDoubleColumnar(unittest.TestCase):

    def test_published_example(self):
        self.assertEqual(
            encrypt_double(
                "THESAMEKEYMUSTNEVERBEUSEDTWICE",
                "ROTOR",
                "ENIGMA"
            ),
            "WCTEIHSTAEVREBEUTMNSUEEDSEEMYK"
        )

    def test_round_trip_with_padding(self):
        message = "THE MESSAGE HAS AN ODD LENGTH"

        ciphertext = encrypt_double(message, "ROTOR", "ENIGMA")
        plaintext = decrypt_double(ciphertext, "ROTOR", "ENIGMA")

        expected = "THEMESSAGEHASANODDLENGTH"
        expected += "X" * ((-len(expected)) % 30)

        self.assertEqual(plaintext, expected)


if __name__ == "__main__":
    unittest.main()

    