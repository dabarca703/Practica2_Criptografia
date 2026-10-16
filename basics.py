def to_numbers(text: str) -> list[int]:
    # Convertimos el texto a mayúsculas.
    text = text.upper()

    # Creamos una lista vacía para guardar los números.
    numbers = []

    # Recorremos las letras y demás caracteres del texto.
    for character in text:
        # Solo aceptamos letras entre A y Z.
        if "A" <= character <= "Z":
            # Calculamos la posición de la letra: A=0, B=1, ..., Z=25.
            number = ord(character) - ord("A")

            # Añadimos ese número al final de la lista.
            numbers.append(number)

    # Devolvemos la lista completa.
    return numbers

def to_letters(nums: list[int]) -> str:
    # Creamos un texto vacío para ir añadiendo las letras.
    text = ""

    # Recorremos los números de la lista.
    for number in nums:
        # Comprobamos que el número pertenece al intervalo permitido.
        if not 0 <= number <= 25:
            raise ValueError(f"El valor {number} debe estar entre 0 y 25")

        # Convertimos la posición del alfabeto en su letra.
        character = chr(number + ord("A"))

        # Añadimos la letra al final del texto.
        text += character

    # Devolvemos el texto completo.
    return text

def egcd(a: int, b: int) -> tuple[int, int, int]:
    # Trabajamos inicialmente con valores absolutos.
    old_r, r = abs(a), abs(b)

    # Coeficientes de abs(a) en los dos restos iniciales.
    old_x, x = 1, 0

    # Coeficientes de abs(b) en los dos restos iniciales.
    old_y, y = 0, 1

    # Repetimos las divisiones hasta que el resto sea cero.
    while r != 0:
        # Calculamos el cociente entero de la división.
        quotient = old_r // r

        # Actualizamos los restos del algoritmo de Euclides.
        old_r, r = r, old_r - quotient * r

        # Actualizamos los coeficientes de abs(a).
        old_x, x = x, old_x - quotient * x

        # Actualizamos los coeficientes de abs(b).
        old_y, y = y, old_y - quotient * y

    # Ajustamos el coeficiente si el primer número era negativo.
    if a < 0:
        old_x = -old_x

    # Ajustamos el coeficiente si el segundo número era negativo.
    if b < 0:
        old_y = -old_y

    # Devolvemos el máximo común divisor y sus dos coeficientes.
    return old_r, old_x, old_y

def modinv(a: int, m: int) -> int:
    # Usamos el valor absoluto del módulo si llega negativo.
    modulus = abs(m)

    # Exigimos que el valor absoluto del módulo sea mayor que uno.
    if modulus <= 1:
        raise ValueError(f"El módulo {m} debe tener valor absoluto mayor que 1")

    # Calculamos el máximo común divisor y los coeficientes de Euclides.
    g, x, y = egcd(a, modulus)

    # El inverso solo existe si el máximo común divisor es uno.
    if g != 1:
        raise ValueError(f"El valor {a} no tiene inverso módulo {m}")

    # Devolvemos el inverso entre cero y modulus - 1.
    return x % modulus

def xor_bytes(data: bytes, key: bytes) -> bytes:
    # Rechazamos una clave vacía porque no se puede repetir.
    if len(key) == 0:
        raise ValueError("La clave XOR no puede estar vacía")

    # Creamos una secuencia de bytes que podemos ir modificando.
    result = bytearray()

    # Recorremos las posiciones de los datos.
    for i in range(len(data)):
        # Seleccionamos un byte de la clave, volviendo al inicio si hace falta.
        key_byte = key[i % len(key)]

        # Aplicamos XOR entre el byte de los datos y el de la clave.
        encrypted_byte = data[i] ^ key_byte

        # Añadimos el resultado.
        result.append(encrypted_byte)

    # Convertimos el resultado al tipo bytes solicitado.
    return bytes(result)
