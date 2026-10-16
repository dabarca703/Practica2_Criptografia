import unittest
from break_vigenere import break_vigenere
from vigenere import encrypt

class TestBreakVigenere(unittest.TestCase):

    def test_break_vigenere_en(self):
        # Prueba de recuperacion de clave en ingles con longitud conocida
        plaintext = (
            "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
            "THISISALONGERTEXTTOENSURETHATSTATISTICALANALYSISWORKSRELIABLY"
            "WHENBREAKINGTHEVIGENERECIPHERWITHAKNOWNKEYLENGTH"
        )
        key = "LEMON"
        ciphertext = encrypt(plaintext, key)
        
        rec_key, rec_plaintext = break_vigenere(ciphertext, m=len(key), language="en")
        
        self.assertEqual(rec_key, key)
        self.assertEqual(rec_plaintext, plaintext)

    def test_break_vigenere_es(self):
        # Prueba de recuperacion de clave en espanol con longitud conocida
        plaintext = (
            "ESTEESUNTEXTOENESPANOLPARAPROBARQUEELATAQUEDEVIGENERE"
            "FUNCIONACORRECTAMENTECUANDOCONOCEMOSLALONGITUDDELACLAVE"
            "YAPLICAMOSANALISISDEFRECUENCIASACADAUNODELOSCOSETS"
        )
        key = "CLAVE"
        ciphertext = encrypt(plaintext, key)
        
        rec_key, rec_plaintext = break_vigenere(ciphertext, m=len(key), language="es")
        
        self.assertEqual(rec_key, key)
        self.assertEqual(rec_plaintext, plaintext)

if __name__ == "__main__":
    unittest.main()


