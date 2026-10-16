# Importamos la herramienta de pruebas.
import unittest

# Importamos el cifrado César para generar criptogramas.
from caesar import encrypt

# Importamos las funciones que vamos a comprobar.
from break_caesar import chi_squared, break_caesar

# Importamos las tablas de frecuencias.
from frequencies import get_frequencies


class TestBreakCaesar(unittest.TestCase):

    def test_break_english_all_keys(self):
        # Usamos un texto inglés suficientemente largo.
        plaintext = (
            "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG "
            "AND THIS MESSAGE CONTAINS ENOUGH ENGLISH LETTERS "
            "TO TEST THE CAESAR BREAKER CORRECTLY"
        )

        # Comprobamos las 26 claves posibles.
        for key in range(26):
            with self.subTest(key=key):
                # Generamos automáticamente el mensaje cifrado.
                ciphertext = encrypt(plaintext, key)

                # Intentamos recuperar su clave y su contenido.
                recovered_key, recovered_text = break_caesar(
                    ciphertext,
                    "en"
                )

                # El ataque debe encontrar la clave utilizada.
                self.assertEqual(recovered_key, key)

                # El texto recuperado debe ser el original normalizado.
                self.assertEqual(
                    recovered_text,
                    "".join(plaintext.split())
                )

    def test_break_spanish_all_keys(self):
        # Utilizamos un texto español suficientemente largo y sin tildes.
        plaintext = (
            "ESTE ES UN MENSAJE EN ESPANOL SUFICIENTEMENTE LARGO "
            "PARA COMPROBAR QUE EL PROGRAMA PUEDE RECUPERAR "
            "LA CLAVE DEL CIFRADO CESAR CORRECTAMENTE"
        )

        # Comprobamos también las 26 claves en español.
        for key in range(26):
            with self.subTest(key=key):
                # Ciframos el texto con la clave actual.
                ciphertext = encrypt(plaintext, key)

                # Ejecutamos el ataque usando la tabla española.
                recovered_key, recovered_text = break_caesar(
                    ciphertext,
                    "es"
                )

                # Comprobamos la clave y el mensaje recuperados.
                self.assertEqual(recovered_key, key)
                self.assertEqual(
                    recovered_text,
                    "".join(plaintext.split())
                )

    def test_score_is_normalized(self):
        # Obtenemos la tabla inglesa.
        table = get_frequencies("en")

        # Repetir exactamente el mismo texto no cambia sus proporciones.
        text = "THISISANENGLISHTEXT"

        # Por eso, la puntuación normalizada debe ser la misma.
        self.assertAlmostEqual(
            chi_squared(text, table),
            chi_squared(text * 5, table),
            places=12
        )

    def test_invalid_language(self):
        # Solo admitimos las tablas inglesa y española.
        with self.assertRaises(ValueError):
            break_caesar("KHOORZRUOG", "fr")

    def test_empty_input(self):
        # No se puede atacar un mensaje que no contiene letras.
        for text in ["", "123 !?"]:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    break_caesar(text, "en")

                with self.assertRaises(ValueError):
                    chi_squared(
                        text,
                        get_frequencies("en")
                    )

                    