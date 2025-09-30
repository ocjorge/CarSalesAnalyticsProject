# generar_queries_pdf.py
import sqlite3
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Conectar a la base de datos
conn = sqlite3.connect("carSales_DB.db")

# Diccionario de queries
queries = {
    "Query01": {
        "sql": """
        SELECT manufacturer, COUNT(*) AS total_sales
        FROM car_sales_vw
        GROUP BY manufacturer
        ORDER BY total_sales DESC;
        """,
        "title": "Fabricantes con mayor número de ventas"
    },
    "Query02": {
        "sql": """
        SELECT model, COUNT(*) AS total_sales
        FROM car_sales_vw
        GROUP BY model
        ORDER BY total_sales DESC;
        """,
        "title": "Modelos más vendidos"
    },
    "Query03": {
        "sql": """
        SELECT year_of_manufacture, AVG(price) AS avg_price
        FROM car_sales_vw
        GROUP BY year_of_manufacture
        ORDER BY year_of_manufacture;
        """,
        "title": "Promedio de precio por año"
    },
    "Query04": {
        "sql": """
        SELECT mileage, price FROM car_sales_vw LIMIT 1000;
        """,
        "title": "Relación entre kilometraje y precio (muestra 1000 filas)"
    },
    "Query05": {
        "sql": """
        SELECT fuel_type, COUNT(*) AS total_sales
        FROM car_sales_vw
        GROUP BY fuel_type;
        """,
        "title": "Distribución de ventas por tipo de combustible"
    }
}

# Función para escribir DataFrame en PDF
def df_to_pdf(c, df, y_start, width_per_col=150):
    y = y_start
    c.setFont("Helvetica", 10)
    
    # Escribir encabezado de columnas
    for i, col in enumerate(df.columns):
        c.drawString(40 + i*width_per_col, y, str(col))
    y -= 15
    
    # Escribir filas
    for _, row in df.iterrows():
        for i, col in enumerate(df.columns):
            text = str(row[col])
            c.drawString(40 + i*width_per_col, y, text)
        y -= 12
        if y < 50:
            c.showPage()
            y = 750
            c.setFont("Helvetica", 10)
    return y

# Crear PDF
pdf_file = "CarSales-QueryOn.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)
width, height = letter
y = height - 40

for qname, qdata in queries.items():
    # Título de la query
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, f"{qname}: {qdata['title']}")
    y -= 25
    
    # Ejecutar query
    df_result = pd.read_sql_query(qdata["sql"], conn)
    
    # Escribir resultados en PDF
    y = df_to_pdf(c, df_result, y)
    y -= 30  # espacio entre queries

c.save()
conn.close()
print(f"✅ PDF '{pdf_file}' generado con todas las queries.")
