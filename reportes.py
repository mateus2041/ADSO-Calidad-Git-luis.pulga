"""
Funciones para generar, exportar y graficar reportes del sistema.
"""

import math
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

reportes_generados = []


def generar_reporte(titulo, datos):
    """Guarda un reporte en memoria con el titulo y los datos proporcionados."""
    if not isinstance(titulo, str) or not titulo.strip() or not datos:
        print("ERROR: el reporte requiere titulo y datos")
        return False

    reporte = {
        "titulo": titulo.strip(),
        "datos": datos.copy() if isinstance(datos, (list, dict)) else datos,
        "estado": "generado",
    }
    reportes_generados.append(reporte)
    print(f"Reporte '{reporte['titulo']}' generado exitosamente")
    return True


def generar_graficos(datos, ruta="grafico.svg"):
    """Genera un grafico de barras SVG para una lista de numeros finitos."""
    if (not isinstance(datos, (list, tuple)) or not datos
            or any(isinstance(valor, bool)
                   or not isinstance(valor, (int, float))
                   or not math.isfinite(valor) for valor in datos)):
        print("ERROR: se requiere una lista de numeros finitos para el grafico")
        return False

    ancho, alto = 640, 400
    margen_izquierdo, margen_superior = 50, 40
    ancho_grafico, alto_grafico = 560, 300
    minimo = min(0, min(datos))
    maximo = max(0, max(datos))
    if minimo == maximo:
        maximo = minimo + 1

    escala = alto_grafico / (maximo - minimo)
    base_y = margen_superior + maximo * escala
    espacio = ancho_grafico / len(datos)
    ancho_barra = espacio * 0.65

    elementos = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" '
        f'height="{alto}" viewBox="0 0 {ancho} {alto}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="320" y="25" text-anchor="middle" '
        'font-family="sans-serif" font-size="18">Grafico de datos</text>',
        f'<line x1="{margen_izquierdo}" y1="{base_y:.2f}" '
        f'x2="{margen_izquierdo + ancho_grafico}" y2="{base_y:.2f}" '
        'stroke="black"/>',
    ]

    for indice, valor in enumerate(datos):
        x = margen_izquierdo + indice * espacio + (espacio - ancho_barra) / 2
        valor_y = margen_superior + (maximo - valor) * escala
        y = min(base_y, valor_y)
        altura = max(abs(base_y - valor_y), 1)
        elementos.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{ancho_barra:.2f}" '
            f'height="{altura:.2f}" fill="#3674b5"/>'
        )
        elementos.append(
            f'<text x="{x + ancho_barra / 2:.2f}" y="{alto - 35}" '
            f'text-anchor="middle" font-family="sans-serif" '
            f'font-size="12">{escape(str(valor))}</text>'
        )

    elementos.append("</svg>")
    Path(ruta).write_text("\n".join(elementos), encoding="utf-8")
    print(f"Grafico SVG generado en '{ruta}'")
    return True


def _texto_pdf(texto):
    """Convierte texto a una cadena literal segura para un flujo PDF."""
    contenido = texto.encode("cp1252", errors="replace")
    escapado = bytearray(b"(")
    for byte in contenido:
        if byte in (ord("("), ord(")"), ord("\\")):
            escapado.extend(b"\\" + bytes((byte,)))
        elif byte < 32 or byte > 126:
            escapado.extend(f"\\{byte:03o}".encode("ascii"))
        else:
            escapado.append(byte)
    escapado.extend(b")")
    return bytes(escapado)


def _crear_pdf(reporte, ruta):
    lineas = [f"Titulo: {reporte['titulo']}", "Datos:"]
    datos = reporte["datos"]
    entradas = datos if isinstance(datos, (list, tuple)) else [datos]
    for dato in entradas:
        lineas.extend(textwrap.wrap(f"- {dato}", width=85) or [""])

    lineas_por_pagina = 48
    paginas = [
        lineas[indice:indice + lineas_por_pagina]
        for indice in range(0, len(lineas), lineas_por_pagina)
    ]
    objetos = {
        1: b"<< /Type /Catalog /Pages 2 0 R >>",
        3: b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
           b"/Encoding /WinAnsiEncoding >>",
    }

    ids_paginas = []
    for numero, lineas_pagina in enumerate(paginas):
        id_pagina = 4 + numero * 2
        id_contenido = id_pagina + 1
        ids_paginas.append(id_pagina)

        comandos = []
        for indice, linea in enumerate(lineas_pagina):
            y = 750 - indice * 15
            comandos.append(
                b"BT /F1 11 Tf 50 " + str(y).encode("ascii")
                + b" Td " + _texto_pdf(linea) + b" Tj ET"
            )
        flujo = b"\n".join(comandos)
        objetos[id_pagina] = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 3 0 R >> >> "
            f"/Contents {id_contenido} 0 R >>"
        ).encode("ascii")
        objetos[id_contenido] = (
            f"<< /Length {len(flujo)} >>\nstream\n".encode("ascii")
            + flujo + b"\nendstream"
        )

    ids = " ".join(f"{id_pagina} 0 R" for id_pagina in ids_paginas)
    objetos[2] = (
        f"<< /Type /Pages /Kids [{ids}] /Count {len(ids_paginas)} >>"
    ).encode("ascii")

    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0] * (max(objetos) + 1)
    for numero in range(1, max(objetos) + 1):
        offsets[numero] = len(pdf)
        pdf.extend(f"{numero} 0 obj\n".encode("ascii"))
        pdf.extend(objetos[numero])
        pdf.extend(b"\nendobj\n")

    inicio_xref = len(pdf)
    pdf.extend(f"xref\n0 {len(offsets)}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\n"
        f"startxref\n{inicio_xref}\n%%EOF\n".encode("ascii")
    )
    Path(ruta).write_bytes(pdf)


def exportar_pdf(titulo, ruta="reporte.pdf"):
    """Exporta a PDF un reporte existente y devuelve si se encontro."""
    for reporte in reportes_generados:
        if reporte["titulo"] == titulo:
            _crear_pdf(reporte, ruta)
            print(f"Reporte '{titulo}' exportado a '{ruta}'")
            return True
    print(f"ERROR: no existe un reporte con titulo '{titulo}'")
    return False


if __name__ == "__main__":
    datos_prueba = [10, 25, 30, 15]
    generar_reporte("Ventas Octubre", datos_prueba)
    generar_graficos(datos_prueba)
    exportar_pdf("Ventas Octubre")
