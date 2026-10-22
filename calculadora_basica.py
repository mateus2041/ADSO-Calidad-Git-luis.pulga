# modulo_calculadora.py - Código espagueti (NIVEL CALAMIDAD 🍝)
import sys

def main():
    print("=== CALCULADORA SENA ===")
    try:
        a = float(input("Numero 1: "))
        b = float(input("Numero 2: "))
        op = input("Operacion (+,-,*,/): ")
        if op == "+":
            print("Resultado:", a + b)
        elif op == "-":
            print("Resultado:", a - b)
        elif op == "*":
            print("Resultado:", a * b)
        elif op == "/":
            if b == 0:
                print("ERROR: Division por cero")
                main()  # 🍝 llamada recursiva como "goto"
            else:
                print("Resultado:", a / b)
        else:
            print("Operacion no valida")
            main()  # 🍝 otra vez goto disfrazado
    except ValueError:
        print("ERROR: debe ingresar numeros")
        main()  # 🍝 y otra...

    fin = input("Otra operacion? (s/n): ")
    if fin == "s":
        main()  # 🍝 ciclo infinito recursivo que revienta la pila
    elif fin == "n":
        sys.exit()
    else:
        print("Opcion invalida, cerrando...")
        sys.exit()

main()  # 🍝 ejecucion directa sin if __name__ == '__main__'
