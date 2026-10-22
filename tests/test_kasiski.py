import unittest

from kasiski import repeats, distances, factor_tally


CIPHERTEXT = (
    "ELQYR JVQDR LXEGB ELQQV ALQFE PTQOG DEZRG SIDSC PEFGO PXDOL "
    "ELQYR JXAOA LPKGV D"
)


class TestKasiski(unittest.TestCase):

    def test_published_repeats(self):
        found = repeats(CIPHERTEXT)

        self.assertEqual(found["ELQ"], [0, 15, 50])
        self.assertEqual(found["ELQYRJ"], [0, 50])

    def test_published_distances(self):
        self.assertEqual(distances(CIPHERTEXT), [15, 35, 50])

    def test_factor_tally(self):
        tally = factor_tally(CIPHERTEXT)

        self.assertEqual(tally[5], 3)
        self.assertEqual(tally[2], 1)
        self.assertEqual(tally[3], 1)

    def test_no_repeats(self):
        self.assertEqual(repeats("ABCDEFG"), {})
        self.assertEqual(distances("ABCDEFG"), [])

    def test_invalid_arguments(self):
        with self.assertRaises(ValueError):
            repeats("ABC", min_len=0)

        with self.assertRaises(ValueError):
            factor_tally("ABC", max_factor=1)


if __name__ == "__main__":
    unittest.main()

    