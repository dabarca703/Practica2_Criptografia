# Importamos la herramienta de pruebas.
import unittest

# Importamos las funciones del cifrado César.
from caesar import encrypt, decrypt

# Importamos las conversiones para calcular el texto normalizado.
from basics import to_numbers, to_letters


class TestCaesar(unittest.TestCase):

    def test_example(self):
        # Comprobamos el cifrado exacto del enunciado.
        self.assertEqual(encrypt("MYSECRETMESSAGE", 3), "PBVHFUHWPHVVDJH")

        # Comprobamos también el descifrado.
        self.assertEqual(decrypt("PBVHFUHWPHVVDJH", 3), "MYSECRETMESSAGE")

    def test_alphabet_wrap(self):
        # Al pasar de la Z, debemos volver a la A.
        self.assertEqual(encrypt("XYZ", 3), "ABC")

        # Al descifrar, podemos pasar de la A hacia la Z.
        self.assertEqual(decrypt("ABC", 3), "XYZ")

    def test_key_values(self):
        # Una clave de 29 equivale a una de 3.
        self.assertEqual(encrypt("ABC", 29), "DEF")
        self.assertEqual(decrypt("DEF", 29), "ABC")

        # Una clave negativa desplaza hacia atrás.
        self.assertEqual(encrypt("ABC", -1), "ZAB")
        self.assertEqual(decrypt("ZAB", -1), "ABC")

        # Una vuelta completa deja las letras igual.
        self.assertEqual(encrypt("ABC", 26), "ABC")

    def test_normalization(self):
        # Eliminamos espacios, signos y números, y usamos mayúsculas.
        self.assertEqual(encrypt("Hola! 123", 3), "KROD")

    def test_edge_cases(self):
        # Un mensaje vacío produce un resultado vacío.
        self.assertEqual(encrypt("", 3), "")
        self.assertEqual(decrypt("", 3), "")

        # Un mensaje sin letras válidas también queda vacío.
        self.assertEqual(encrypt("123 !?", 3), "")
        self.assertEqual(decrypt("123 !?", 3), "")

        # Comprobamos un mensaje de una sola letra.
        self.assertEqual(encrypt("A", 3), "D")
        self.assertEqual(decrypt("D", 3), "A")

    def test_round_trip(self):
        # Probamos distintos mensajes.
        messages = [
            "",
            "A",
            "Hola, mundo!",
            "123 !?",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        ]

        # Probamos claves negativas, normales y mayores que 25.
        for k in range(-30, 31):
            for message in messages:
                with self.subTest(k=k, message=message):
                    # Calculamos cómo debe quedar el mensaje normalizado.
                    expected = to_letters(to_numbers(message))

                    # Ciframos el mensaje y después lo desciframos.
                    encrypted = encrypt(message, k)
                    recovered = decrypt(encrypted, k)

                    # Debemos recuperar el mensaje normalizado.
                    self.assertEqual(recovered, expected)
                    