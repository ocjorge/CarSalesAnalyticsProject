import pandas as pd
import sqlite3
import kagglehub
import os

# Descargar el dataset de Kaggle a una carpeta local
# Esto creará una carpeta en tu sistema con el nombre del dataset
path = kagglehub.dataset_download("msnbehdani/mock-dataset-of-second-hand-car-sales")
print(f"Path to dataset files: {path}")

# Cargar el archivo CSV desde la ruta de descarga
df = pd.read_csv(os.path.join(path, 'car_sales_data.csv'))

# Conectar a la base de datos (si no existe, se creará un archivo .db nuevo)
conn = sqlite3.connect('car_sales_DB.db')
cursor = conn.cursor()

# Opcional: Eliminar las tablas si ya existen para un proceso limpio
cursor.execute("DROP TABLE IF EXISTS cars;")
cursor.execute("DROP TABLE IF EXISTS models;")
cursor.execute("DROP TABLE IF EXISTS manufacturers;")
conn.commit()

# Crear la tabla de fabricantes con el nombre como clave primaria
cursor.execute('''
CREATE TABLE manufacturers (
    manufacturer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
''')

# Crear la tabla de modelos, con un ID autoincremental y una clave foránea a fabricantes
cursor.execute('''
CREATE TABLE models (
    model_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    manufacturer_id INTEGER NOT NULL,
    engine_size REAL NOT NULL,
    fuel_type TEXT NOT NULL,
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(manufacturer_id)
);
''')

# Crear la tabla de autos, con una clave foránea a modelos
cursor.execute('''
CREATE TABLE cars (
    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL,
    year_of_manufacture INTEGER NOT NULL,
    mileage INTEGER NOT NULL,
    price INTEGER NOT NULL,
    FOREIGN KEY (model_id) REFERENCES models(model_id)
);
''')

print("Tablas creadas exitosamente.")
conn.commit()
