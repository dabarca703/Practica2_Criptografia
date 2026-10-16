# break_vigenere.py

from vigenere import cosets, decrypt
from break_caesar import break_caesar
from basics import to_letters

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

