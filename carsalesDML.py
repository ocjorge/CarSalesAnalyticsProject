# Crea el archivo CarSales-DML
import pandas as pd
import sqlite3
import kagglehub
import os


if os.path.exists(csv_local):
    df = pd.read_csv(csv_local)
else:
    # Intentar descargar (requiere kagglehub)
    path = kagglehub.dataset_download("msnbehdani/mock-dataset-of-second-hand-car-sales")
    df = pd.read_csv(os.path.join(path, "car_sales_data.csv"))

# Normalizar strings y evitar NaN
df['Manufacturer'] = df['Manufacturer'].astype(str).str.strip()
df['Model'] = df['Model'].astype(str).str.strip()
df['Fuel type'] = df['Fuel type'].astype(str).str.strip()
# Asegurarse de que Engine size, Year, Mileage, Price sean numéricos cuando corresponda
# (si tu CSV ya tiene tipos correctos, esto no cambia nada)
df['Engine size'] = pd.to_numeric(df['Engine size'], errors='coerce').fillna(0)
df['Year of manufacture'] = pd.to_numeric(df['Year of manufacture'], errors='coerce').fillna(0).astype(int)
df['Mileage'] = pd.to_numeric(df['Mileage'], errors='coerce').fillna(0).astype(int)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0).astype(int)

# ---------- Conectar a la BD ----------
db_path = "carSales_DB.db"   # usa el mismo nombre que usas en tu script que funciona
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ---------- Crear/abrir archivo DML SQL ----------
out_sql = "CarSales-DML.sql"
f = open(out_sql, "w", encoding="utf-8")
f.write("BEGIN TRANSACTION;\n\n")

# ---------- Insertar fabricantes en BD y escribir SQL ----------
manufacturer_id_map = {}
manufacturers = df['Manufacturer'].unique().tolist()
f.write("-- Insertar fabricantes\n")
for m in manufacturers:
    m_clean = m.strip()
    safe_m = m_clean.replace("'", "''")   # para SQL literal
    # escribir línea SQL idempotente
    f.write(f"INSERT OR IGNORE INTO manufacturers (name) VALUES ('{safe_m}');\n")
    # ejecutar en la BD (parametrizado)
    cursor.execute("INSERT OR IGNORE INTO manufacturers (name) VALUES (?)", (m_clean,))
    # obtener el id (existe ya o se acaba de crear)
    cursor.execute("SELECT manufacturer_id FROM manufacturers WHERE name = ?", (m_clean,))
    manufacturer_id = cursor.fetchone()[0]
    manufacturer_id_map[m_clean] = manufacturer_id
f.write("\n")

# ---------- Insertar modelos en BD y escribir SQL ----------
models_df = df[['Manufacturer', 'Model', 'Engine size', 'Fuel type']].drop_duplicates()
model_id_map = {}
f.write("-- Insertar modelos\n")
for _, row in models_df.iterrows():
    man = str(row['Manufacturer']).strip()
    model = str(row['Model']).strip()
    engine = row['Engine size']
    fuel = str(row['Fuel type']).strip()

    safe_man = man.replace("'", "''")
    safe_model = model.replace("'", "''")
    safe_fuel = fuel.replace("'", "''")

    # escribir línea SQL (usa SELECT para obtener manufacturer_id)
    f.write(
        "INSERT OR IGNORE INTO models (name, manufacturer_id, engine_size, fuel_type)\n"
        f"SELECT '{safe_model}', manufacturer_id, {engine}, '{safe_fuel}' FROM manufacturers WHERE name = '{safe_man}';\n"
    )

    # ejecutar inserción en la BD (parametrizada y segura)
    cursor.execute(
        "INSERT OR IGNORE INTO models (name, manufacturer_id, engine_size, fuel_type) "
        "VALUES (?, (SELECT manufacturer_id FROM manufacturers WHERE name = ?), ?, ?)",
        (model, man, engine, fuel)
    )

    # Obtener model_id (ya existente o recién insertado)
    cursor.execute(
        "SELECT model_id FROM models WHERE name = ? AND manufacturer_id = (SELECT manufacturer_id FROM manufacturers WHERE name = ?) AND engine_size = ? AND fuel_type = ?",
        (model, man, engine, fuel)
    )
    rowid = cursor.fetchone()
    if rowid:
        model_id = rowid[0]
    else:
        # por seguridad, intentar obtener con una consulta menos específica
        cursor.execute("SELECT model_id FROM models WHERE name = ? LIMIT 1", (model,))
        model_id = cursor.fetchone()[0]
    model_id_map[(man, model, engine, fuel)] = model_id
f.write("\n")

# ---------- Insertar autos en BD (batch) y escribir SQL ----------
f.write("-- Insertar autos\n")
cars_to_insert = []
count_rows = 0
for _, row in df.iterrows():
    man = str(row['Manufacturer']).strip()
    model = str(row['Model']).strip()
    engine = row['Engine size']
    fuel = str(row['Fuel type']).strip()
    year = int(row['Year of manufacture'])
    mileage = int(row['Mileage'])
    price = int(row['Price'])

    safe_man = man.replace("'", "''")
    safe_model = model.replace("'", "''")
    safe_fuel = fuel.replace("'", "''")

    # Escribir la sentencia SQL que localizará el model_id y hará el insert (fácil de ejecutar en SQLite CLI)
    f.write(
        f"INSERT INTO cars (model_id, year_of_manufacture, mileage, price)\n"
        f"SELECT model_id, {year}, {mileage}, {price} FROM models JOIN manufacturers USING(manufacturer_id)\n"
        f"WHERE models.name = '{safe_model}' AND manufacturers.name = '{safe_man}' AND models.engine_size = {engine} AND models.fuel_type = '{safe_fuel}';\n"
    )

    # Para insertar en la BD ahora mismo, usamos el model_id obtenido en model_id_map
    key = (man, model, engine, fuel)
    if key in model_id_map:
        model_id = model_id_map[key]
    else:
        # como fallback, intentar consultar en BD por si el key no está en el map
        cursor.execute(
            "SELECT model_id FROM models WHERE name = ? AND manufacturer_id = (SELECT manufacturer_id FROM manufacturers WHERE name = ?) AND engine_size = ? AND fuel_type = ? LIMIT 1",
            (model, man, engine, fuel)
        )
        res = cursor.fetchone()
        if res:
            model_id = res[0]
            model_id_map[key] = model_id
        else:
            # Si no encontró, saltar (esto no debería pasar si el flujo es correcto)
            continue

    cars_to_insert.append((model_id, year, mileage, price))
    count_rows += 1

f.write("\nCOMMIT;\n")
f.close()  # cerramos el archivo SQL

# Insertar los autos en batch (ejecución real en la BD)
if cars_to_insert:
    cursor.executemany(
        "INSERT INTO cars (model_id, year_of_manufacture, mileage, price) VALUES (?, ?, ?, ?)",
        cars_to_insert
    )

conn.commit()
conn.close()

print("Inserciones en BD completadas.")
print(f" - Fabricantes procesados: {len(manufacturers)}")
print(f" - Modelos procesados: {len(models_df)}")
print(f" - Autos preparados para insertar: {count_rows}")
print(f"Archivo SQL generado: {out_sql}")
