# Fuentes de los porcentajes:
# https://www.sttmedia.com/characterfrequency-english
# https://www.sttmedia.com/characterfrequency-spanish
# Autor: Stefan Trost, tablas de frecuencias de WordCreator.
# Conservamos solo A-Z y renormalizamos sus valores.


# Porcentajes de las letras en inglés.
EN_PERCENT = {
    "A": 8.34, "B": 1.54, "C": 2.73, "D": 4.14,
    "E": 12.60, "F": 2.03, "G": 1.92, "H": 6.11,
    "I": 6.71, "J": 0.23, "K": 0.87, "L": 4.24,
    "M": 2.53, "N": 6.80, "O": 7.70, "P": 1.66,
    "Q": 0.09, "R": 5.68, "S": 6.11, "T": 9.37,
    "U": 2.85, "V": 1.06, "W": 2.34, "X": 0.20,
    "Y": 2.04, "Z": 0.06,
}


# Porcentajes de las letras A-Z en español.
ES_PERCENT = {
    "A": 11.72, "B": 1.49, "C": 3.87, "D": 4.67,
    "E": 13.72, "F": 0.69, "G": 1.00, "H": 1.18,
    "I": 5.28, "J": 0.52, "K": 0.11, "L": 5.24,
    "M": 3.08, "N": 6.83, "O": 8.44, "P": 2.89,
    "Q": 1.11, "R": 6.41, "S": 7.20, "T": 4.60,
    "U": 4.55, "V": 1.05, "W": 0.04, "X": 0.14,
    "Y": 1.09, "Z": 0.47,
}


def get_frequencies(language: str) -> dict[str, float]:
    # Seleccionamos los porcentajes del idioma solicitado.
    if language == "en":
        percentages = EN_PERCENT
    elif language == "es":
        percentages = ES_PERCENT
    else:
        # Rechazamos los idiomas que no están disponibles.
        raise ValueError(f"Idioma no válido: {language}. Usa 'en' o 'es'")

    # Sumamos los porcentajes de las 26 letras seleccionadas.
    total = sum(percentages.values())

    # Creamos un diccionario para guardar las proporciones.
    frequencies = {}

    # Recorremos cada letra y su porcentaje.
    for letter, percentage in percentages.items():
        # Dividimos entre el total para que las proporciones sumen uno.
        frequencies[letter] = percentage / total

    # Devolvemos la tabla normalizada.
    return frequencies

