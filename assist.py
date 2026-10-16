# assist.py

from collections import Counter

# Frecuencias esperadas de mayor a menor en ingles y espanol
EXPECTED_FREQ = {
    "en": "ETAOINSRHLDCUMFPGWYBVKXJQZ",
    "es": "EAOSRNIDLCTUMPBGVYQHFZJNXK"
}

def report(ciphertext: str, language: str = "en") -> str:
    """
    Genera un informe estadistico para ayudar al criptoanalisis manual.
    """
    if not ciphertext:
        return "No ciphertext provided."
        
    length = len(ciphertext)
    output = []
    
    # 1. Conteo, porcentaje y comparacion de letras
    counts = Counter(ciphertext)
    ranked_letters = [char for char, _ in counts.most_common()]
    
    output.append("--- LETTER FREQUENCIES ---")
    output.append(f"{'Letter':<10}{'Count':<10}{'%':<10}{'Expected':<10}")
    
    expected = EXPECTED_FREQ.get(language, EXPECTED_FREQ["en"])
    
    for i, char in enumerate(ranked_letters):
        count = counts[char]
        pct = (count / length) * 100
        exp_char = expected[i] if i < len(expected) else "-"
        output.append(f"{char:<10}{count:<10}{pct:<10.2f}{exp_char:<10}")
        
    # 2. Mapeo inicial sugerido por alineacion de rangos
    output.append("\n--- SUGGESTED MAPPING ---")
    mapping = {}
    for i, char in enumerate(ranked_letters):
        if i < len(expected):
            mapping[char] = expected[i]
            
    sorted_mapping = sorted(mapping.items())
    output.append("Cipher: " + "".join([k for k, v in sorted_mapping]))
    output.append("Plain : " + "".join([v for k, v in sorted_mapping]))
    
    # 3. Trigramas repetidos
    output.append("\n--- REPEATED TRIGRAMS ---")
    trigrams = {}
    for i in range(len(ciphertext) - 2):
        tri = ciphertext[i:i+3]
        if tri not in trigrams:
            trigrams[tri] = []
        trigrams[tri].append(i)
        
    repeated_trigrams = {k: v for k, v in trigrams.items() if len(v) > 1}
    for tri, positions in sorted(repeated_trigrams.items(), key=lambda item: len(item[1]), reverse=True):
        output.append(f"{tri}: {len(positions)} times at positions {positions}")
        
    # 4. Los 10 bigramas mas frecuentes
    output.append("\n--- TOP 10 BIGRAMS ---")
    bigrams = Counter([ciphertext[i:i+2] for i in range(len(ciphertext) - 1)])
    for bi, count in bigrams.most_common(10):
        output.append(f"{bi}: {count}")
        
    # 5. Letras dobles
    output.append("\n--- DOUBLED LETTERS ---")
    doubles = Counter()
    for i in range(len(ciphertext) - 1):
        if ciphertext[i] == ciphertext[i+1]:
            doubles[ciphertext[i:i+2]] += 1
            
    for double, count in doubles.most_common():
        output.append(f"{double}: {count}")
        
    return "\n".join(output)

if __name__ == "__main__":
    # Criptograma de 110 letras de la guia para realizar el Report Task
    crypto = (
        "QATNTYSMHQXJOCYHKATMFSNQITUTMPTKTIPJIDTTKHIGQATCEG"
        "JMHQAFNTYMTORTYCSNTJIEXQATDTXYCIRTYACIGTPVATIHOHNY"
        "JFKMJFHNTΡ".replace('Ρ', 'P')  # Reemplazo de seguridad por si es letra griega
    )
    print(report(crypto, language="en"))

    