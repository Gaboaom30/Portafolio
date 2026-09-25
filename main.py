from pipeline_ventas import extraer_datos_csv, transformar_datos, generar_resumen, guardar_resultado


def main():
    """Punto de entrada del pipeline."""
    print("=" * 50)
    print("  PIPELINE DE VENTAS DIARIAS")
    print("=" * 50)

    #configuracion
    ruta_entrada = "data/ventas_dia.csv"
    ruta_salida = "data/resumen_dia.json"
    ruta_errores = "data/errores_dia.json"

    #Exract
    print("\n[EXTRACT] Extrayendo datos del CSV...")
    ventas_raw = extraer_datos_csv(ruta_entrada)
    print(f"Se extrajeron {len(ventas_raw)} registros.")

    #transform
    print("\n[TRANSFORM] Transformando datos...")
    ventas_limpias, errores = transformar_datos(ventas_raw)
    tasa_exito = (len(ventas_limpias) / len(ventas_raw)) * 100 if ventas_raw else 0
    print(f"Se limpiaron {len(ventas_limpias)} registros. Tasa de éxito: {tasa_exito:.2f}%")
    print(f"Se encontraron {len(errores)} errores.")

    #analyze
    print("\n[ANALYZE] Generando resumen...")
    resumen = generar_resumen(ventas_limpias)
    print(f"Total facturado: {resumen['total_facturado']:.2f}")

    #load
    print("\n[LOAD] Guardando resultados...")
    guardar_resultado(resumen, errores, ruta_salida, ruta_errores)
    print(f"Resumen: {ruta_salida}")
    if errores:
        print(f"Errores: {ruta_errores}")

    #Reporte final
    print("\n" + "=" * 50)
    print("  RESUMEN EJECUTIVO")
    print("=" * 50)
    print(f"  Facturación total: {resumen['total_facturado']}€")
    print(f"  Ticket medio:      {resumen['ticket_medio']}€")
    print(f"  Transacciones:     {resumen['num_transacciones']}")
    print(f"  Clientes únicos:   {resumen['clientes_unicos']}")
    print(f"\n  Top 3 productos:")
    for item in resumen["top_3_productos"]:
        print(f"    • {item['producto']}: {item['total']}€")
    print("=" * 50)


if __name__ == "__main__":
    main()