from basics import to_numbers, to_letters
from keylength import coset_ic
from vigenere import encrypt


with open("data/reference_en.txt", encoding="utf-8") as file:
    plaintext = to_letters(to_numbers(file.read()))

# Usamos las primeras 1.000 letras para que la tabla sea manejable.
plaintext = plaintext[:1000]

key = "LEMON"
ciphertext = encrypt(plaintext, key)

true_length = len(key)
divisors = [m for m in range(1, true_length + 1) if true_length % m == 0]
multiples = [
    m for m in range(1, 17)
    if m % true_length == 0
]

print(f"Longitud verdadera de la clave: {true_length}")
print("m | IC medio | marca")
print("--|----------|------")

for m in range(1, 17):
    marks = []

    if m in divisors:
        marks.append("divisor")
    if m == true_length:
        marks.append("longitud verdadera")
    elif m in multiples:
        marks.append("múltiplo")

    print(f"{m:2} | {coset_ic(ciphertext, m):.6f} | {', '.join(marks)}")

    