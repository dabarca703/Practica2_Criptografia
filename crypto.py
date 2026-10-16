# crypto.py

import sys
import argparse

# Importamos todos los modulos que hemos creado
import caesar
import affine
import monoalpha
import vigenere
import break_caesar
import break_affine
import break_vigenere
import assist

def normalize(text: str) -> str:
    """Normaliza el texto: mayusculas y solo letras A-Z"""
    return ''.join(c for c in text.upper() if 'A' <= c <= 'Z')

def main():
    # Opciones comunes (archivos de entrada/salida y lenguaje)
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("--in", dest="in_file", help="Archivo de entrada")
    parent_parser.add_argument("--out", dest="out_file", help="Archivo de salida")
    parent_parser.add_argument("--lang", choices=["en", "es"], default="en", help="Idioma (en/es)")

    parser = argparse.ArgumentParser(description="Herramienta CLI de Criptografia")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Parser para CAESAR
    p_caesar = subparsers.add_parser("caesar", parents=[parent_parser])
    p_caesar.add_argument("mode", choices=["encrypt", "decrypt"])
    p_caesar.add_argument("--key", type=int, required=True)

    # Parser para AFFINE
    p_affine = subparsers.add_parser("affine", parents=[parent_parser])
    p_affine.add_argument("mode", choices=["encrypt", "decrypt"])
    p_affine.add_argument("--a", type=int, required=True)
    p_affine.add_argument("--b", type=int, required=True)

    # Parser para MONOALPHA
    p_mono = subparsers.add_parser("mono", parents=[parent_parser])
    p_mono.add_argument("mode", choices=["encrypt", "decrypt"])
    p_mono.add_argument("--keyword", type=str, required=True)

    # Parser para VIGENERE
    p_vigenere = subparsers.add_parser("vigenere", parents=[parent_parser])
    p_vigenere.add_argument("mode", choices=["encrypt", "decrypt"])
    p_vigenere.add_argument("--key", type=str, required=True)

    # Parser para BREAK (ataques)
    p_break = subparsers.add_parser("break")
    break_subs = p_break.add_subparsers(dest="cipher", required=True)

    b_caesar = break_subs.add_parser("caesar", parents=[parent_parser])
    b_affine = break_subs.add_parser("affine", parents=[parent_parser])
    b_vig = break_subs.add_parser("vigenere", parents=[parent_parser])
    b_vig.add_argument("--m", type=int, required=True)

    # Parser para ASSIST
    p_assist = subparsers.add_parser("assist", parents=[parent_parser])

    # Parsear argumentos y manejar salida limpia de errores de consola
    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit(2)

    try:
        # Leer entrada (desde archivo o desde la consola/stdin)
        if args.in_file:
            with open(args.in_file, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            text = sys.stdin.read()

        # Normalizamos siempre la entrada para evitar problemas de formato
        text = normalize(text)
        result = ""

        # Ejecucion de cada comando
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

        elif args.command == "break":
            if args.cipher == "caesar":
                key, plaintext = break_caesar.break_caesar(text, args.lang)
                result = f"Key: {key}\nPlaintext: {plaintext}"
            elif args.cipher == "affine":
                key, plaintext = break_affine.break_affine(text, args.lang)
                result = f"Key: (a={key[0]}, b={key[1]})\nPlaintext: {plaintext}"
            elif args.cipher == "vigenere":
                key, plaintext = break_vigenere.break_vigenere(text, args.m, args.lang)
                result = f"Key: {key}\nPlaintext: {plaintext}"

        elif args.command == "assist":
            result = assist.report(text, args.lang)

        # Escribir salida (a archivo o a consola)
        if args.out_file:
            with open(args.out_file, 'w', encoding='utf-8') as f:
                f.write(result + '\n')
        else:
            sys.stdout.write(result + '\n')

    # Captura general de errores sin volcar Stack Traces feos (requisito de la guia)
    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()

    