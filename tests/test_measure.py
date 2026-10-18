import unittest

from measure import index_of_coincidence


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


if __name__ == "__main__":
    unittest.main()

    