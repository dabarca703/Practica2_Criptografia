# Importamos la herramienta de pruebas.
import unittest

# Importamos las funciones del cifrado afín.
from affine import encrypt, decrypt, valid_keys

# Importamos las conversiones para normalizar los mensajes.
from basics import to_numbers, to_letters


class TestAffine(unittest.TestCase):

    def test_example(self):
        # Comprobamos el cifrado publicado en el enunciado.
        self.assertEqual(encrypt("attack", 5, 8), "IZZISG")

        # Comprobamos que el descifrado recupera el mensaje.
        self.assertEqual(decrypt("IZZISG", 5, 8), "ATTACK")

    def test_valid_keys(self):
        # Estos son los valores de a que son coprimos con 26.
        valid_a = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

        # Construimos el conjunto de parejas que esperamos.
        expected = {(a, b) for a in valid_a for b in range(26)}

        # Obtenemos las claves generadas por nuestra función.
        keys = valid_keys()

        # Debe haber exactamente 312 parejas.
        self.assertEqual(len(keys), 312)

        # Deben ser todas las parejas esperadas, sin que falte ninguna.
        self.assertEqual(set(keys), expected)

    def test_invalid_keys(self):
        # Estos valores de a no tienen inverso módulo 26.
        for a in [0, 2, 13, 26, -2]:
            with self.subTest(a=a):
                # El cifrado debe rechazar la clave.
                with self.assertRaises(ValueError):
                    encrypt("HOLA", a, 8)

                # El descifrado también debe rechazarla.
                with self.assertRaises(ValueError):
                    decrypt("HOLA", a, 8)

    def test_equivalent_keys(self):
        # 31 equivale a 5, y 34 equivale a 8, módulo 26.
        self.assertEqual(encrypt("attack", 31, 34), "IZZISG")
        self.assertEqual(decrypt("IZZISG", 31, 34), "ATTACK")

        # -21 equivale a 5, y -18 equivale a 8, módulo 26.
        self.assertEqual(encrypt("attack", -21, -18), "IZZISG")
        self.assertEqual(decrypt("IZZISG", -21, -18), "ATTACK")

    def test_edge_cases(self):
        # Los mensajes vacíos deben producir resultados vacíos.
        self.assertEqual(encrypt("", 5, 8), "")
        self.assertEqual(decrypt("", 5, 8), "")

        # Los mensajes sin letras válidas también quedan vacíos.
        self.assertEqual(encrypt("123 !?", 5, 8), "")
        self.assertEqual(decrypt("123 !?", 5, 8), "")

        # La A vale 0: (5 * 0 + 8) % 26 = 8, que corresponde a I.
        self.assertEqual(encrypt("A", 5, 8), "I")
        self.assertEqual(decrypt("I", 5, 8), "A")

        # Una clave inválida debe rechazarse incluso con un mensaje vacío.
        with self.assertRaises(ValueError):
            encrypt("", 2, 8)

        with self.assertRaises(ValueError):
            decrypt("", 2, 8)

    def test_round_trip(self):
        # Probamos mensajes de distintos tipos.
        messages = [
            "",
            "A",
            "Hola, mundo! 123",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        ]

        # Comprobamos las 312 parejas de claves válidas.
        for a, b in valid_keys():
            for message in messages:
                with self.subTest(a=a, b=b, message=message):
                    # Calculamos el mensaje normalizado que esperamos.
                    expected = to_letters(to_numbers(message))

                    # Ciframos y después desciframos con las mismas claves.
                    encrypted = encrypt(message, a, b)
                    recovered = decrypt(encrypted, a, b)

                    # Debemos recuperar el mensaje normalizado.
                    self.assertEqual(recovered, expected)

                    