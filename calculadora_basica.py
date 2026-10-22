# calculadora_basica.py - Calculadora basica

import math


def main():
    while True:
        print("=== CALCULADORA SENA ===")
        try:
            a = float(input("Numero 1: "))
            b = float(input("Numero 2: "))
        except ValueError:
            print("ERROR: debe ingresar numeros")
            continue

        if not math.isfinite(a) or not math.isfinite(b):
            print("ERROR: ingrese numeros finitos")
            continue

        op = input("Operacion (+,-,*,/): ").strip()
        if op == "+":
            resultado = a + b
        elif op == "-":
            resultado = a - b
        elif op == "*":
            resultado = a * b
        elif op == "/":
            if b == 0:
                print("ERROR: Division por cero")
                continue
            resultado = a / b
        else:
            print("Operacion no valida")
            continue

        if not math.isfinite(resultado):
            print("ERROR: resultado fuera de rango")
            continue

        print("Resultado:", resultado)
        while True:
            fin = input("Otra operacion? (s/n): ").strip().lower()
            if fin == "s":
                break
            if fin == "n":
                return
            print("Opcion invalida, ingrese s o n")


if __name__ == "__main__":
    main()
