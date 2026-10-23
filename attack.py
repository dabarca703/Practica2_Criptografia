import argparse
from pathlib import Path

from assist import report
from basics import to_letters, to_numbers
from break_columnar import attack as attack_columnar
from break_columnar import _bigram_score, _load_bigram_scores
from break_vigenere import attack as attack_vigenere
from keylength import coset_ic, find_key_length
from measure import classify, index_of_coincidence


IC_THRESHOLD = 0.055


def main():
    parser = argparse.ArgumentParser(
        description="Ataque automático de cifrados clásicos"
    )
    parser.add_argument("--in", dest="input_file", required=True)
    parser.add_argument("--lang", choices=["en", "es"], default="en")
    parser.add_argument("--cols", type=int)
    args = parser.parse_args()

    ciphertext = Path(args.input_file).read_text(encoding="utf-8")
    normalized = to_letters(to_numbers(ciphertext))

    if not normalized:
        parser.error("El archivo no contiene letras A-Z")

    ic = index_of_coincidence(normalized)
    family = classify(normalized, language=args.lang)

    print(f"Longitud normalizada: {len(normalized)}")
    print(f"Índice de coincidencia: {ic:.6f}")
    print(f"Familia detectada: {family}")

    if family == "substitution":
        print(f"Umbral de IC usado: {IC_THRESHOLD:.3f}")

        if ic >= IC_THRESHOLD:
            print("Tipo: sustitución monoalfabética")
            print(report(normalized, language=args.lang))
        else:
            print("Tipo: sustitución polialfabética")
            for m in range(1, min(16, len(normalized)) + 1):
                print(f"IC medio para m={m}: {coset_ic(normalized, m):.6f}")

            key_length = find_key_length(normalized, language=args.lang)
            print(f"Longitud de clave elegida: {key_length}")

            key, plaintext = attack_vigenere(
                normalized,
                language=args.lang
            )
            print(f"Clave: {key}")
            print(f"Texto: {plaintext}")

        return

    if args.cols is not None:
        if not 2 <= args.cols <= 8:
            parser.error("--cols debe estar entre 2 y 8")
        candidates = [args.cols]
    else:
        candidates = [
            n for n in range(2, 9)
            if len(normalized) % n == 0
        ]

    if not candidates:
        parser.error(
            "No hay divisores entre 2 y 8; indica --cols si conoces "
            "el número de columnas"
        )

    scores = _load_bigram_scores(args.lang)
    best = None

    for n_cols in candidates:
        if len(normalized) % n_cols != 0:
            parser.error(
                f"La longitud del texto no es divisible por {n_cols} columnas"
            )

        order, plaintext = attack_columnar(
            normalized,
            n_cols=n_cols,
            language=args.lang
        )
        score = _bigram_score(plaintext, scores)

        print(
            f"{n_cols} columnas: puntuación={score:.6f}, "
            f"orden={order}"
        )

        if best is None or score > best[0]:
            best = (score, n_cols, order, plaintext)

    score, n_cols, order, plaintext = best
    print(
        f"Mejor candidato: {n_cols} columnas, orden={order}, "
        f"puntuación={score:.6f}"
    )
    print(f"Texto: {plaintext}")


if __name__ == "__main__":
    main()

    
