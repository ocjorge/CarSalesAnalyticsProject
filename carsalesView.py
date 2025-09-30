#Crear Vista con python
import sqlite3
import pandas as pd

# Usa el mismo nombre de BD que en los scripts DDL/DML
conn = sqlite3.connect("carSales_DB.db")
cursor = conn.cursor()

cursor.execute("DROP VIEW IF EXISTS car_sales_vw;")
cursor.execute('''
CREATE VIEW car_sales_vw AS
SELECT 
    c.car_id,
    m.name AS model,
    mf.name AS manufacturer,
    m.engine_size,
    m.fuel_type,
    c.year_of_manufacture,
    c.mileage,
    c.price
FROM cars c
JOIN models m ON c.model_id = m.model_id
JOIN manufacturers mf ON m.manufacturer_id = mf.manufacturer_id;
''')
conn.commit()

# Exportar vista a CSV
df_vw = pd.read_sql_query("SELECT * FROM car_sales_vw;", conn)
df_vw.to_csv("CarSales.csv", index=False)

conn.close()
print("Vista exportada a CarSales.csv")
