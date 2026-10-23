import sys
import argparse

import caesar
import affine
import monoalpha
import vigenere
import break_caesar
import break_affine
import break_vigenere
import assist
import railfence
import columnar
import measure
import kasiski


def normalize(text: str) -> str:
    """Pasa el texto a mayúsculas y conserva solo letras A-Z."""
    return "".join(c for c in text.upper() if "A" <= c <= "Z")


def main():
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("--in", dest="in_file", help="Archivo de entrada")
    parent_parser.add_argument("--out", dest="out_file", help="Archivo de salida")
    parent_parser.add_argument(
        "--lang", choices=["en", "es"], default="en", help="Idioma"
    )

    parser = argparse.ArgumentParser(description="Herramienta CLI de criptografía")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_caesar = subparsers.add_parser("caesar", parents=[parent_parser])
    p_caesar.add_argument("mode", choices=["encrypt", "decrypt"])
    p_caesar.add_argument("--key", type=int, required=True)

    p_affine = subparsers.add_parser("affine", parents=[parent_parser])
    p_affine.add_argument("mode", choices=["encrypt", "decrypt"])
    p_affine.add_argument("--a", type=int, required=True)
    p_affine.add_argument("--b", type=int, required=True)

    p_mono = subparsers.add_parser("mono", parents=[parent_parser])
    p_mono.add_argument("mode", choices=["encrypt", "decrypt"])
    p_mono.add_argument("--keyword", required=True)

    p_vigenere = subparsers.add_parser("vigenere", parents=[parent_parser])
    p_vigenere.add_argument("mode", choices=["encrypt", "decrypt"])
    p_vigenere.add_argument("--key", required=True)

    p_railfence = subparsers.add_parser("railfence", parents=[parent_parser])
    p_railfence.add_argument("mode", choices=["encrypt", "decrypt"])
    p_railfence.add_argument("--rails", type=int, required=True)

    p_columnar = subparsers.add_parser("columnar", parents=[parent_parser])
    p_columnar.add_argument("mode", choices=["encrypt", "decrypt"])
    p_columnar.add_argument("--key", required=True)
    p_columnar.add_argument("--pad", default="X")

    p_break = subparsers.add_parser("break")
    break_subs = p_break.add_subparsers(dest="cipher", required=True)

    b_caesar = break_subs.add_parser("caesar", parents=[parent_parser])
    b_affine = break_subs.add_parser("affine", parents=[parent_parser])
    b_vigenere = break_subs.add_parser("vigenere", parents=[parent_parser])
    b_vigenere.add_argument("--m", type=int, required=True)

    p_assist = subparsers.add_parser("assist", parents=[parent_parser])

    p_measure = subparsers.add_parser("measure", parents=[parent_parser])
    p_measure.add_argument("measure_kind", choices=["ic", "classify", "kasiski"])

    args = parser.parse_args()

    try:
        if args.in_file:
            with open(args.in_file, "r", encoding="utf-8") as file:
                text = file.read()
        else:
            text = sys.stdin.read()

        text = normalize(text)
        result = ""

        if args.command == "caesar":
            if args.mode == "encrypt":
                result = caesar.encrypt(text, args.key)
            else:
                result = caesar.decrypt(text, args.key)

        elif args.command == "affine":
            if args.mode == "encrypt":
                result = affine.encrypt(text, args.a, args.b)
            else:
                result = affine.decrypt(text, args.a, args.b)

        elif args.command == "mono":
            key = monoalpha.key_from_keyword(args.keyword)
            if args.mode == "encrypt":
                result = monoalpha.encrypt(text, key)
            else:
                result = monoalpha.decrypt(text, key)

        elif args.command == "vigenere":
            if args.mode == "encrypt":
                result = vigenere.encrypt(text, args.key)
            else:
                result = vigenere.decrypt(text, args.key)

        elif args.command == "railfence":
            if args.mode == "encrypt":
                result = railfence.encrypt(text, args.rails)
            else:
                result = railfence.decrypt(text, args.rails)

        elif args.command == "columnar":
            if args.mode == "encrypt":
                result = columnar.encrypt(text, args.key, pad=args.pad)
            else:
                result = columnar.decrypt(text, args.key)

        elif args.command == "break":
            if args.cipher == "caesar":
                key, plaintext = break_caesar.break_caesar(text, args.lang)
                result = f"Key: {key}\nPlaintext: {plaintext}"
            elif args.cipher == "affine":
                key, plaintext = break_affine.break_affine(text, args.lang)
                result = (
                    f"Key: (a={key[0]}, b={key[1]})\n"
                    f"Plaintext: {plaintext}"
                )
            elif args.cipher == "vigenere":
                key, plaintext = break_vigenere.break_vigenere(
                    text, args.m, args.lang
                )
                result = f"Key: {key}\nPlaintext: {plaintext}"

        elif args.command == "assist":
            result = assist.report(text, args.lang)

        elif args.command == "measure":
            if args.measure_kind == "ic":
                result = f"IC: {measure.index_of_coincidence(text):.6f}"
            elif args.measure_kind == "classify":
                result = measure.classify(text, language=args.lang)
            else:
                result = (
                    f"Repeticiones: {kasiski.repeats(text)}\n"
                    f"Distancias: {kasiski.distances(text)}\n"
                    f"Votos por factor: {kasiski.factor_tally(text)}"
                )

        if args.out_file:
            with open(args.out_file, "w", encoding="utf-8") as file:
                file.write(result + "\n")
        else:
            print(result)

    except Exception as error:
        sys.stderr.write(f"Error: {error}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

    