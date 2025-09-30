CREATE TABLE manufacturers (
    manufacturer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE models (
    model_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    manufacturer_id INTEGER NOT NULL,
    engine_size REAL NOT NULL,
    fuel_type TEXT NOT NULL,
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(manufacturer_id)
);

CREATE TABLE cars (
    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL,
    year_of_manufacture INTEGER NOT NULL,
    mileage INTEGER NOT NULL,
    price INTEGER NOT NULL,
    FOREIGN KEY (model_id) REFERENCES models(model_id)
);
