# Importamos la herramienta de pruebas incluida en Python.
import unittest

# Importamos las cinco funciones que queremos comprobar.
from basics import to_numbers, to_letters, egcd, modinv, xor_bytes


# Agrupamos las pruebas de las funciones básicas.
class TestBasics(unittest.TestCase):

    def test_to_numbers(self):
        # Comprobamos mayúsculas, minúsculas y eliminación de signos.
        self.assertEqual(to_numbers("Hola! 123"), [7, 14, 11, 0])

        # Comprobamos los extremos del alfabeto.
        self.assertEqual(to_numbers("Az"), [0, 25])

        # Un texto vacío o sin letras válidas devuelve una lista vacía.
        self.assertEqual(to_numbers(""), [])
        self.assertEqual(to_numbers("123 ! ñá"), [])

    def test_to_letters(self):
        # Comprobamos la conversión de números a letras.
        self.assertEqual(to_letters([7, 14, 11, 0]), "HOLA")
        self.assertEqual(to_letters([0, 25]), "AZ")

        # Una lista vacía debe devolver un texto vacío.
        self.assertEqual(to_letters([]), "")

        # Los números fuera del intervalo deben producir ValueError.
        for number in [-1, 26]:
            with self.assertRaises(ValueError):
                to_letters([number])

    def test_conversion_round_trip(self):
        # Convertir a números y volver a letras recupera el texto normalizado.
        result = to_letters(to_numbers("Hola, mundo!"))
        self.assertEqual(result, "HOLAMUNDO")

    def test_egcd(self):
        # Cada caso contiene a, b y su máximo común divisor esperado.
        cases = [
            (5, 26, 1),
            (12, 18, 6),
            (-12, 18, 6),
            (12, -18, 6),
            (-12, -18, 6),
            (0, 7, 7),
            (7, 0, 7),
            (0, 0, 0),
        ]

        # Comprobamos el máximo común divisor y la igualdad de Bézout.
        for a, b, expected_g in cases:
            with self.subTest(a=a, b=b):
                g, x, y = egcd(a, b)
                self.assertEqual(g, expected_g)
                self.assertEqual(a * x + b * y, g)

    def test_modinv(self):
        # Comprobamos los tres resultados publicados en el enunciado.
        self.assertEqual(modinv(5, 26), 21)
        self.assertEqual(modinv(7, 26), 15)
        self.assertEqual(modinv(17, 26), 23)

        # Comprobamos entradas negativas según nuestra convención.
        self.assertEqual(modinv(-5, 26), 5)
        self.assertEqual(modinv(5, -26), 21)

    def test_modinv_invalid(self):
        # Estos valores no tienen inverso módulo 26.
        for a in [13, 2, 0]:
            # También comprobamos que el mensaje menciona el valor.
            with self.assertRaisesRegex(ValueError, str(a)):
                modinv(a, 26)

        # Nuestra función rechaza los módulos 0, 1 y -1.
        for m in [0, 1, -1]:
            with self.assertRaises(ValueError):
                modinv(5, m)

    def test_xor_example(self):
        # Comprobamos el resultado exacto del enunciado.
        result = xor_bytes(b"HELLO", b"KEYKE")
        self.assertEqual(result.hex(), "030015070a")

        # Una clave más corta debe repetirse hasta cubrir los datos.
        self.assertEqual(xor_bytes(b"HELLO", b"KEY"), result)

    def test_xor_round_trip(self):
        # Incluimos datos vacíos, un byte y todos los valores posibles de byte.
        for data in [b"", b"A", b"HELLO", bytes(range(256))]:
            for key in [b"K", b"KEY", b"CLAVE LARGA"]:
                encrypted = xor_bytes(data, key)

                # Aplicar XOR dos veces con la misma clave recupera los datos.
                self.assertEqual(xor_bytes(encrypted, key), data)

    def test_xor_empty_key(self):
        # Una clave vacía debe rechazarse, incluso con datos vacíos.
        for data in [b"HELLO", b""]:
            with self.assertRaises(ValueError):
                xor_bytes(data, b"")
                