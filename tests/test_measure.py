import unittest

from measure import index_of_coincidence, classify 


class TestIndexOfCoincidence(unittest.TestCase):

    def test_published_values(self):
        self.assertAlmostEqual(
            index_of_coincidence("CRYPTANALYSIS"),
            6 / 156,
            places=4
        )

        self.assertAlmostEqual(
            index_of_coincidence("THEINDEXOFCOINCIDENCE"),
            34 / 420,
            places=4
        )

    def test_normalization(self):
        self.assertAlmostEqual(
            index_of_coincidence("The index of coincidence!"),
            index_of_coincidence("THEINDEXOFCOINCIDENCE"),
            places=10
        )

    def test_short_inputs(self):
        self.assertEqual(index_of_coincidence(""), 0.0)
        self.assertEqual(index_of_coincidence("A"), 0.0)

           
    def test_classify_transposition(self):
        text = (
            "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
            "THISISALONGERENGLISHTEXTFORTESTING"
            "LETTERFREQUENCIESINACOLUMNARTRANSPOSITION"
        )

        ciphertext = __import__("columnar").encrypt(text, "CIPHER")
        self.assertEqual(classify(ciphertext), "transposition")

    def test_classify_substitution(self):
        from monoalpha import encrypt as monoalpha_encrypt
        from monoalpha import key_from_keyword

        text = (
            "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
            "THISISALONGERENGLISHTEXTFORTESTING"
            "LETTERFREQUENCIESINASUBSTITUTIONCIPHER"
        )

        key = key_from_keyword("CIPHER")
        ciphertext = monoalpha_encrypt(text, key)

        self.assertEqual(classify(ciphertext), "substitution")

    def test_classify_empty_text(self):
        with self.assertRaises(ValueError):
            classify("123 !")


if __name__ == "__main__":
    unittest.main()

