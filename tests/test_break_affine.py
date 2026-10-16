# Importamos la herramienta de pruebas.
import unittest

# Importamos el cifrado afín y sus claves válidas.
from affine import encrypt, valid_keys

# Importamos el ataque que queremos comprobar.
from break_affine import break_affine


class TestBreakAffine(unittest.TestCase):

    def test_break_english_generated_ciphertexts(self):
        # Texto inglés de una longitud en la que el ataque funciona bien.
        plaintext = (
            "THIS IS A SUFFICIENTLY LONG ENGLISH MESSAGE USED TO "
            "CHECK WHETHER THE AFFINE CIPHER BREAKER CAN RECOVER "
            "THE CORRECT KEY AUTOMATICALLY FROM LETTER FREQUENCIES"
        )

        # Seleccionamos 24 claves repartidas por el espacio de 312 claves.
        selected_keys = valid_keys()[::13]

        # Generamos y atacamos al menos 20 criptogramas.
        for a, b in selected_keys:
            with self.subTest(a=a, b=b):
                # Ciframos con la pareja actual.
                ciphertext = encrypt(plaintext, a, b)

                # Intentamos recuperar la clave.
                recovered_key, recovered_text = break_affine(
                    ciphertext,
                    "en"
                )

                # Comprobamos la clave exacta.
                self.assertEqual(recovered_key, (a, b))

                # Comprobamos el mensaje normalizado.
                self.assertEqual(
                    recovered_text,
                    "".join(plaintext.split())
                )

    def test_break_spanish(self):
        # Texto español suficientemente largo.
        plaintext = (
            "ESTE ES UN MENSAJE EN ESPANOL SUFICIENTEMENTE LARGO "
            "PARA COMPROBAR EL ATAQUE AUTOMATICO CONTRA EL CIFRADO "
            "AFIN UTILIZANDO LAS FRECUENCIAS DE LAS LETRAS"
        )

        # Comprobamos varias claves españolas.
        keys = [(1, 4), (5, 8), (7, 15), (17, 3), (25, 20)]

        for a, b in keys:
            with self.subTest(a=a, b=b):
                ciphertext = encrypt(plaintext, a, b)

                recovered_key, recovered_text = break_affine(
                    ciphertext,
                    "es"
                )

                self.assertEqual(recovered_key, (a, b))
                self.assertEqual(
                    recovered_text,
                    "".join(plaintext.split())
                )

    def test_invalid_language(self):
        # Rechazamos cualquier idioma distinto de en o es.
        with self.assertRaises(ValueError):
            break_affine("ABCDEF", "fr")

    def test_empty_input(self):
        # Rechazamos textos vacíos o sin letras válidas.
        for text in ["", "123 !?"]:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    break_affine(text, "en")

                    