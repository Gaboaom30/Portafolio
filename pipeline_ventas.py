import csv
import json
from datetime import datetime
from collections import defaultdict

#Extract
def extraer_datos_csv(ruta_csv):
    "Extrae los datos de un archivo CSV y los devuelve como una lista de diccionarios."
    with open(ruta_csv, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

#Transform
def transformar_datos(ventas_raw):
    "Limpia datos sucios y calcula totales, devuelve limpios y errores"
    limpias = []
    errores = []
    for i, venta in enumerate(ventas_raw):
        try:
            # Validar y limpiar datos
             if not venta.get("producto", "").strip():
                raise ValueError("Producto vacío")

             cantidad_raw = venta.get("cantidad", "").strip()
             cantidad = int(cantidad_raw) if cantidad_raw else 1

             precio = float(venta["precio_unitario"])  # Esto puede lanzar ValueError si no es convertible
             total = cantidad * precio

             limpias.append({
                 'fecha': venta["fecha"],
                 'producto': venta["producto"].strip(),
                 'categoria': venta["categoria"].strip(),
                 'cantidad': cantidad,
                 'precio_unitario': precio,
                 'total': round(total, 2),
                 'cliente': venta["cliente"].strip()
             })
        except (ValueError, TypeError) as e:
            errores.append({
                "fila": i + 2,
                "error": str(e),
                "datos": dict(venta)
            })  # +2 para compensar encabezado y base 0
    return limpias, errores

# ANALYZE
def generar_resumen(ventas_limpias):
    if not ventas_limpias:
        return {"error": "No hay datos limpios para analizar."}
    
    #Metricas generales
    total_facturado = sum(venta['total'] for venta in ventas_limpias)
    num_transacciones = len(ventas_limpias)
    ticket_medio = total_facturado / num_transacciones if num_transacciones else 0

    #Por categoria
    por_categoria = defaultdict(lambda: {'total': 0, 'transacciones': 0})
    for venta in ventas_limpias:
        categoria = venta['categoria']
        por_categoria[categoria]['total'] += venta['total']
        por_categoria[categoria]['transacciones'] += 1

    #Top productos
    productos_total = defaultdict(float)
    for venta in ventas_limpias:
        productos_total[venta['producto']] += venta['total']

    # Ordenar productos por total facturado
    top_productos = sorted(productos_total.items(), key=lambda x: x[1], reverse=True)[:3]

    #clientes unicos
    clientes = set(venta['cliente'] for venta in ventas_limpias)

    return {
        "fecha_reporte": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_facturado": round(total_facturado, 2),
        "num_transacciones": num_transacciones,
        "ticket_medio": round(ticket_medio, 2),
        "clientes_unicos": len(clientes),
        "por_categoria": dict(por_categoria),
        "top_3_productos": [{"producto": p, "total": round(t, 2)} for p, t in top_productos],
    }

#LOAD
def guardar_resultado(resumen, errores, ruta_salida, ruta_errores):
    """Escribe el resumen y los errores en archivos JSON."""
    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(resumen, f, indent=2, ensure_ascii=False)
    
    if errores:
        with open(ruta_errores, "w", encoding="utf-8") as f:
            json.dump(errores, f, indent=2, ensure_ascii=False)