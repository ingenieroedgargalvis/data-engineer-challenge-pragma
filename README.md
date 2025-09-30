# data-engineer-challenge-pragma
"Solución al reto de Ingeniería de Datos de Pragma con PostgreSQL y Python

### 📖 Descripción  
Este proyecto implementa un **pipeline de datos en Python con PostgreSQL** que procesa archivos CSV en **micro-batches**, los almacena en base de datos y mantiene estadísticas incrementales sobre el campo `price`:  

- Número total de filas (`count`)  
- Precio promedio (`avg`)  
- Precio mínimo (`min`)  
- Precio máximo (`max`)  

Se procesan inicialmente los archivos `2012-1.csv` hasta `2012-5.csv`, y luego se ejecuta un archivo de validación `validation.csv`.  

---

## 📊 Flujo del Pipeline  

```mermaid
flowchart LR
    A[Archivos CSV<br>(2012-1.csv ... 2012-5.csv,<br>validation.csv)] --> B[Python Pipeline]
    B -->|Inserción por micro-batches| C[(PostgreSQL<br>Tabla: transacciones)]
    B --> D[Estadísticas en memoria<br>(count, avg, min, max)]
    C --> E[Consulta final en BD<br>COUNT, AVG, MIN, MAX]
    D --> E
```

---

## ⚙️ Requerimientos  

### 1. Base de datos PostgreSQL  
- Usuario: `postgres`  
- Contraseña: `MiClaveSegura2025`  
- Base de datos: `PRAGMA`  
- Puerto: `5432`  
 

### 2. Python y librerías  
Requiere **Python 3.9+** y las siguientes dependencias:  

```bash
pip install -r requirements.txt
```

Archivo `requirements.txt`:  
```
pandas==2.2.2
sqlalchemy==2.0.31
psycopg2-binary==2.9.9
```

---

## 📂 Estructura del proyecto  

```
data-engineer-challenge-pragma/
│
├── CSV_Data/               
|              ├── 2012-1.csv
│              ├── 2012-2.csv
│              ├── 2012-3.csv
│              ├── 2012-4.csv
│              └── 2012-5.csv
|── validation.csv
│
├── pipeline.py    # Script principal con el pipeline
├── requirements.txt        # Dependencias del proyecto
├── README.md               # Leer Este archivo
└── .gitignore              # Ignora CSV, venv, pycache, etc.
```

---

## ▶️ Ejecución del pipeline  

1. Clonar el repositorio:  
   ```bash
   git clone https://github.com/ingenieroedgargalvis/data-engineer-challenge-pragma.git
   cd data-engineer-challenge-pragma
   ```

2. Crear la base de datos `PRAGMA` en PostgreSQL (si no existe).  

3. Instalar dependencias:  
   ```bash
   pip install -r requirements.txt
   ```

4. Colocar los archivos CSV en la carpeta `CSV_Data/`. y el archivo de validacion en la carpeta raiz

5. Ejecutar el la conexion a postgreesql.py pipeline:  
   ```bash
   python conexionpostgresql.py
   python pipeline.py
   ```

---

## 📊 Resultados esperados  

Durante la ejecución se mostrarán estadísticas en consola, por ejemplo:  

```
📄 Procesando archivo: 2012-1.csv
--- Estadísticas al finalizar 2012-1.csv ---
Total de filas cargadas: 5000
Precio promedio: 123.45
Precio mínimo: 10.0
Precio máximo: 999.9
--------------------------------------

🔍 Verificación en BD después de la carga inicial
Resultados de la consulta a la BD:
 total_filas  promedio_precio  minimo_precio  maximo_precio
      25000           456.78            10.0          1200.5
```

---

## 🛠️ Tecnologías utilizadas  
- **Python 3**  
- **pandas** (lectura de CSV y micro-batches)  
- **SQLAlchemy** (conexión a PostgreSQL)  
- **PostgreSQL** (almacenamiento de datos)  

---

## 👨‍💻 Autor  
- [Edgar Gerardo Galvis] – Solución al reto de Ingeniería de Datos de **Pragma**  
