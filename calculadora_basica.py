def main():
    while True:
        print("=== CALCULADORA SENA ===")
        try:
            a = float(input("Numero 1: "))
            b = float(input("Numero 2: "))
        except ValueError:
            print("ERROR: debe ingresar numeros")
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
