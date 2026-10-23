# break_vigenere.py

from vigenere import cosets, decrypt
from break_caesar import break_caesar
from keylength import find_key_length
from basics import to_numbers, to_letters


def break_vigenere(ciphertext: str, m: int, language: str = "en") -> tuple[str, str]:
    # Validar que la longitud de clave sea valida
    if m <= 0:
        raise ValueError("Key length must be a positive integer.")
    
    # Dividir el texto cifrado en m cosets
    c_cosets = cosets(ciphertext, m)
    
    # Aplicar break_caesar a cada coset independientemente
    key_shifts = []
    for coset in c_cosets:
        shift, _ = break_caesar(coset, language=language)
        key_shifts.append(shift)
        
    # Reconstruir la clave a partir de los desplazamientos
    key = to_letters(key_shifts)
    
    # Descifrar el texto completo usando la clave recuperada
    plaintext = decrypt(ciphertext, key)
    
    return key, plaintext

def attack(ciphertext: str, language: str = "en") -> tuple[str, str]:
    """Estima la longitud de clave y devuelve (clave, texto descifrado)."""
    normalized = to_letters(to_numbers(ciphertext))

    if not normalized:
        raise ValueError("El texto cifrado debe contener letras A-Z")

    key_length = find_key_length(normalized, language=language)
    key, plaintext = break_vigenere(
        normalized,
        key_length,
        language=language
    )

    return key, plaintext



