# Importamos la herramienta de pruebas.
import unittest

# Importamos las funciones del cifrado monoalfabético.
from monoalpha import encrypt, decrypt, key_from_keyword

# Importamos las conversiones para normalizar los mensajes.
from basics import to_numbers, to_letters


class TestMonoalpha(unittest.TestCase):

    def test_examples(self):
        # Utilizamos la clave de los ejemplos del enunciado.
        key = "MNBVCXZASDFGHJKLPOIUYTREWQ"

        # Comprobamos los dos mensajes cifrados publicados.
        self.assertEqual(encrypt("HELLO", key), "ACGGK")
        self.assertEqual(encrypt("BOB", key), "NKN")

        # Comprobamos también sus descifrados.
        self.assertEqual(decrypt("ACGGK", key), "HELLO")
        self.assertEqual(decrypt("NKN", key), "BOB")

    def test_keyword_example(self):
        # Comprobamos la clave generada que aparece en el enunciado.
        self.assertEqual(
            key_from_keyword("CRYPTO"),
            "CRYPTOABDEFGHIJKLMNQSUVWXZ"
        )

    def test_keyword_repeated_letters(self):
        # BANANA aporta primero las letras B, A y N, sin repetir.
        self.assertEqual(
            key_from_keyword("banana! 123"),
            "BANCDEFGHIJKLMOPQRSTUVWXYZ"
        )

        # Sin letras en la palabra clave, obtenemos el alfabeto ordenado.
        self.assertEqual(
            key_from_keyword(""),
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )

    def test_invalid_keys(self):
        # Incluimos claves vacías, cortas, repetidas y con caracteres inválidos.
        invalid_keys = [
            "",
            "ABC",
            "A" * 26,
            "ABCDEFGHIJKLMNOPQRSTUVWXY1",
            "abcdefghijklmnopqrstuvwxyz",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ!",
        ]

        # Todas deben rechazarse al cifrar y al descifrar.
        for key in invalid_keys:
            with self.subTest(key=key):
                with self.assertRaises(ValueError):
                    encrypt("HELLO", key)

                with self.assertRaises(ValueError):
                    decrypt("HELLO", key)

    def test_edge_cases(self):
        # Utilizamos una clave válida para comprobar mensajes especiales.
        key = "MNBVCXZASDFGHJKLPOIUYTREWQ"

        # Los mensajes vacíos deben devolver un texto vacío.
        self.assertEqual(encrypt("", key), "")
        self.assertEqual(decrypt("", key), "")

        # Los mensajes sin letras válidas también quedan vacíos.
        self.assertEqual(encrypt("123 !?", key), "")
        self.assertEqual(decrypt("123 !?", key), "")

        # Comprobamos un mensaje de una sola letra.
        self.assertEqual(encrypt("A", key), "M")
        self.assertEqual(decrypt("M", key), "A")

        # Comprobamos la normalización de un mensaje.
        self.assertEqual(encrypt("Hello! 123", key), "ACGGK")

        # Una clave inválida se rechaza incluso con mensajes vacíos.
        with self.assertRaises(ValueError):
            encrypt("", "ABC")

        with self.assertRaises(ValueError):
            decrypt("", "ABC")

    def test_round_trip(self):
        # Probamos tres alfabetos de sustitución distintos.
        keys = [
            "MNBVCXZASDFGHJKLPOIUYTREWQ",
            "ZYXWVUTSRQPONMLKJIHGFEDCBA",
            key_from_keyword("CRYPTO"),
        ]

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
                    # Calculamos el texto normalizado esperado.
                    expected = to_letters(to_numbers(message))

                    # Aplicamos el cifrado y su operación inversa.
                    encrypted = encrypt(message, key)
                    recovered = decrypt(encrypted, key)

                    # Comprobamos que recuperamos el texto esperado.
                    self.assertEqual(recovered, expected)

                    
