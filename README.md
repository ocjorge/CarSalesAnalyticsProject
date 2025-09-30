# 🚗 Car Sales Analytics Project

Este proyecto procesa y analiza datos de ventas de automóviles de segunda mano, creando una base de datos estructurada y generando reportes analíticos.

## 📊 Descripción

El sistema descarga un dataset de Kaggle sobre ventas de automóviles usados, lo transforma en un esquema de base de datos relacional normalizado (SQLite) y genera consultas analíticas con visualización en PDF.

## 🛠️ Características

- **Descarga automática** de dataset desde Kaggle
- **Base de datos normalizada** con 3 tablas principales
- **Limpieza y transformación** de datos
- **Generación de consultas SQL** analíticas
- **Reportes en PDF** con resultados de consultas

## 📁 Estructura del Proyecto

```
car-sales-analytics/
├── car_sales_etl.py          # Script principal ETL
├── generar_queries_pdf.py    # Generador de reportes PDF
├── carSales_DB.db           # Base de datos SQLite
├── CarSales-DML.sql         # Script SQL con inserciones
└── CarSales-QueryOn.pdf     # Reporte analítico PDF
```

## 🗃️ Esquema de Base de Datos

```sql
manufacturers (manufacturer_id, name)
models (model_id, name, manufacturer_id, engine_size, fuel_type)
cars (car_id, model_id, year_of_manufacture, mileage, price)
```

## 📈 Consultas Analíticas

1. **Fabricantes con mayor número de ventas**
2. **Modelos más vendidos** 
3. **Promedio de precio por año**
4. **Relación entre kilometraje y precio**
5. **Distribución de ventas por tipo de combustible**

## 🚀 Instalación y Uso

### Prerrequisitos
```bash
pip install pandas sqlite3 kagglehub reportlab
```

### Configuración Kaggle
1. Crear cuenta en [Kaggle](https://www.kaggle.com/)
2. Configurar API token en `~/.kaggle/kaggle.json`

### Ejecución
```bash
# Procesar datos y crear base de datos
python car_sales_etl.py

# Generar reporte analítico PDF
python generar_queries_pdf.py
```

## 📊 Tecnologías Utilizadas

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-orange.svg)
![SQLite](https://img.shields.io/badge/SQLite-Database-green.svg)
![Kaggle](https://img.shields.io/badge/Kaggle-Dataset-purple.svg)
![ReportLab](https://img.shields.io/badge/ReportLab-PDF_Generation-red.svg)

## 📋 Dataset

- **Fuente**: [Kaggle - Mock Dataset of Second Hand Car Sales](https://www.kaggle.com/msnbehdani/mock-dataset-of-second-hand-car-sales)
- **Contenido**: Datos simulados de ventas de automóviles usados
- **Campos**: Fabricante, Modelo, Año, Kilometraje, Precio, Tipo de Combustible

## 🎯 Resultados

El proyecto genera:
- ✅ Base de datos SQLite normalizada
- ✅ Script DML con todas las inserciones
- ✅ Reporte PDF con análisis de ventas
- ✅ Consultas optimizadas para business intelligence

## 📄 Licencia

Este proyecto es para fines educativos. Los datos pertenecen al dataset original de Kaggle.

---

**Desarrollado como proyecto de análisis de datos y ETL**
