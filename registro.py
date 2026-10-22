"""
=========================================
MODULO DE REGISTRO DE USUARIOS - ADSO
=========================================
Descripcion:
    Permite registrar usuarios en el sistema con validacion
    de campos obligatorios y formato de correo electronico.

Funciones principales:
    - registrar_usuario(): Registra un usuario con sus datos.
    - validar_correo(): Verifica que el correo tenga formato valido.

Autor: Aprendiz A
Version: 1.0
Fecha: Octubre 2026
"""

import re

usuarios_registrados = []


def validar_correo(correo):
    """Valida que el correo tenga formato correcto."""
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if re.match(patron, correo):
        return True
    print(f"ERROR: el correo '{correo}' no es valido")
    return False


def registrar_usuario(nombre, correo, contrasena):
    """Registra un nuevo usuario en el sistema."""
    if not nombre or not correo or not contrasena:
        print("ERROR: todos los campos son obligatorios")
        return False

    if not validar_correo(correo):
        return False

    usuarios_registrados.append({
        "nombre": nombre,
        "correo": correo,
        "contrasena": contrasena
    })
    print(f"Usuario '{nombre}' registrado exitosamente")
    return True


if __name__ == "__main__":
    registrar_usuario("Juan Perez", "juan@correo.com", "1234")
    registrar_usuario("Maria Lopez", "correo_invalido", "abcd")  # Debe fallar
