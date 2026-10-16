# Importamos las funciones básicas que ya hemos programado.
from basics import to_numbers, to_letters, egcd, modinv


def encrypt(plaintext: str, a: int, b: int) -> str:
    # Comprobamos que a tiene inverso módulo 26.
    # Si no lo tiene, modinv lanza ValueError.
    modinv(a, 26)

    # Reducimos ambas claves al intervalo de 0 a 25.
    a = a % 26
    b = b % 26

    # Normalizamos el texto y convertimos sus letras en números.
    numbers = to_numbers(plaintext)

    # Creamos una lista para guardar el resultado.
    encrypted = []

    # Recorremos los números del mensaje.
    for number in numbers:
        # Aplicamos la fórmula del cifrado afín.
        encrypted_number = (a * number + b) % 26

        # Guardamos el número cifrado.
        encrypted.append(encrypted_number)

    # Convertimos el resultado en letras.
    return to_letters(encrypted)


def decrypt(ciphertext: str, a: int, b: int) -> str:
    # Calculamos el inverso de a y comprobamos que la clave sea válida.
    inverse_a = modinv(a, 26)

    # Reducimos b al intervalo de 0 a 25.
    b = b % 26

    # Convertimos el texto cifrado en números.
    numbers = to_numbers(ciphertext)

    # Creamos una lista para guardar el mensaje recuperado.
    decrypted = []

    # Recorremos los números cifrados.
    for number in numbers:
        # Deshacemos la suma y la multiplicación del cifrado.
        decrypted_number = (inverse_a * (number - b)) % 26

        # Guardamos el número recuperado.
        decrypted.append(decrypted_number)

    # Convertimos el resultado en letras.
    return to_letters(decrypted)


def valid_keys() -> list[tuple[int, int]]:
    # Creamos una lista para las parejas de claves válidas.
    keys = []

    # Recorremos los posibles valores de a entre 0 y 25.
    for a in range(26):
        # Calculamos el máximo común divisor de a y 26.
        g, x, y = egcd(a, 26)

        # Solo aceptamos a si tiene inverso módulo 26.
        if g == 1:
            # Para cada a válido, cualquier b entre 0 y 25 sirve.
            for b in range(26):
                # Guardamos la pareja de claves.
                keys.append((a, b))

    # Devolvemos todas las parejas válidas.
    return keys
