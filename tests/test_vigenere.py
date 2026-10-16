# Importamos la herramienta de pruebas.
import unittest

# Importamos las funciones de Vigenère.
from vigenere import encrypt, decrypt, cosets

# Importamos las conversiones para normalizar los mensajes.
from basics import to_numbers, to_letters


class TestVigenere(unittest.TestCase):

    def test_examples(self):
        # Comprobamos los dos cifrados publicados en el enunciado.
        self.assertEqual(encrypt("MYSECRETMESSAGE", "KEY"), "WCQOGPOXKOWQKKC")
        self.assertEqual(encrypt("attackatdawn", "LEMON"), "LXFOPVEFRNHR")

        # Comprobamos también los descifrados.
        self.assertEqual(decrypt("WCQOGPOXKOWQKKC", "KEY"), "MYSECRETMESSAGE")
        self.assertEqual(decrypt("LXFOPVEFRNHR", "LEMON"), "ATTACKATDAWN")

    def test_invalid_keys(self):
        # Estas claves están vacías o contienen caracteres no permitidos.
        invalid_keys = ["", "KEY1", "KE Y", "KEY!", "NIÑO", "Á"]

        # Todas deben rechazarse al cifrar y al descifrar.
        for key in invalid_keys:
            with self.subTest(key=key):
                with self.assertRaises(ValueError):
                    encrypt("HELLO", key)

                with self.assertRaises(ValueError):
                    decrypt("HELLO", key)

        # Una clave vacía también debe rechazarse si el mensaje está vacío.
        with self.assertRaises(ValueError):
            encrypt("", "")

        with self.assertRaises(ValueError):
            decrypt("", "")

    def test_normalization(self):
        # La clave puede escribirse en minúsculas.
        # Los espacios y signos del mensaje no deben consumir posiciones de clave.
        self.assertEqual(
            encrypt("Attack at dawn! 123", "lemon"),
            "LXFOPVEFRNHR"
        )

        # El texto cifrado también se normaliza antes de descifrar.
        self.assertEqual(
            decrypt("lxfopv efrnhr!", "lemon"),
            "ATTACKATDAWN"
        )

    def test_edge_cases(self):
        # Los mensajes vacíos producen resultados vacíos con una clave válida.
        self.assertEqual(encrypt("", "KEY"), "")
        self.assertEqual(decrypt("", "KEY"), "")

        # Los mensajes sin letras válidas también quedan vacíos.
        self.assertEqual(encrypt("123 !?", "KEY"), "")
        self.assertEqual(decrypt("123 !?", "KEY"), "")

        # Un mensaje de una letra utiliza solo la primera letra de la clave.
        self.assertEqual(encrypt("A", "KEY"), "K")
        self.assertEqual(decrypt("K", "KEY"), "A")

        # Comprobamos otro mensaje más corto que la clave.
        self.assertEqual(encrypt("AB", "LEMON"), "LF")
        self.assertEqual(decrypt("LF", "LEMON"), "AB")

    def test_cosets(self):
        # Comprobamos el ejemplo del enunciado.
        self.assertEqual(cosets("ABCDEF", 3), ["AD", "BE", "CF"])

        # Los grupos pueden tener tamaños diferentes.
        self.assertEqual(cosets("ABCDEFG", 3), ["ADG", "BE", "CF"])

        # Si m supera la longitud del texto, algunos grupos quedan vacíos.
        self.assertEqual(cosets("AB", 4), ["A", "B", "", ""])

        # Un texto vacío produce m grupos vacíos.
        self.assertEqual(cosets("", 3), ["", "", ""])

        # Con m igual a uno, todo el mensaje queda en un solo grupo.
        self.assertEqual(cosets("ABC", 1), ["ABC"])

    def test_invalid_coset_length(self):
        # Rechazamos longitudes que no sean enteros positivos.
        for m in [0, -1, 2.5]:
            with self.subTest(m=m):
                with self.assertRaises(ValueError):
                    cosets("ABCDEF", m)

    def test_round_trip(self):
        # Probamos claves de diferentes longitudes.
        keys = ["A", "KEY", "LEMON", "CLAVELARGA"]

        # Probamos mensajes vacíos, cortos y con todo el alfabeto.
        messages = [
            "",
            "A",
            "Hola, mundo! 123",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        ]

        # Ciframos y desciframos cada mensaje con cada clave.
        for key in keys:
            for message in messages:
                with self.subTest(key=key, message=message):
                    # Calculamos el mensaje normalizado esperado.
                    expected = to_letters(to_numbers(message))

                    # Aplicamos el cifrado y su operación inversa.
                    encrypted = encrypt(message, key)
                    recovered = decrypt(encrypted, key)

                    # Comprobamos que recuperamos el mensaje esperado.
                    self.assertEqual(recovered, expected)
                    