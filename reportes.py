"""
=========================================
MODULO DE REPORTES - ADSO
=========================================
Descripcion:
    Permite generar reportes del sistema con exportacion a PDF
    y visualizacion de graficos estadisticos.

Funciones principales:
    - generar_reporte(): Crea un reporte con datos del sistema.
    - exportar_pdf(): Exporta el reporte a formato PDF.
    - generar_graficos(): Genera graficos estadisticos.

Autor: Aprendiz B
Version: 1.0
Fecha: Octubre 2026
"""

reportes_generados = []


def generar_reporte(titulo, datos):
    """Genera un reporte con el titulo y datos proporcionados."""
    if not titulo or not datos:
        print("ERROR: el reporte requiere titulo y datos")
        return False

    reporte = {
        "titulo": titulo,
        "datos": datos,
        "estado": "generado"
    }
    reportes_generados.append(reporte)
    print(f"Reporte '{titulo}' generado exitosamente")
    return True


def generar_graficos(datos):
    """Genera graficos estadisticos a partir de los datos."""
    if not datos:
        print("ERROR: no hay datos para generar graficos")
        return False
    print(f"Grafico generado con {len(datos)} registros")
    return True


def exportar_pdf(titulo):
    """Exporta un reporte existente a formato PDF."""
    for reporte in reportes_generados:
        if reporte["titulo"] == titulo:
            print(f"Reporte '{titulo}' exportado a PDF")
            return True
    print(f"ERROR: no existe un reporte con titulo '{titulo}'")
    return False


if __name__ == "__main__":
    datos_prueba = [10, 25, 30, 15]
    generar_reporte("Ventas Octubre", datos_prueba)
    generar_graficos(datos_prueba)
    exportar_pdf("Ventas Octubre")
