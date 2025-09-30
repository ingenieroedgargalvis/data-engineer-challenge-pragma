
#----********************Solución para el reto de Ingeniería de Datos de Pragma con PostgreSQL.**************************--


import pandas as pd
from sqlalchemy import create_engine, text

# ***--- 1. CONFIGURACIÓN DE LA CONEXIÓN A POSTGRESQL ---***

# los datos de conexión
usuario = "postgres"
clave = "MiClaveSegura2025"
host = "localhost"
puerto = "5432"
base_datos = "PRAGMA"

#  URL de conexión previamente probada
url_conexion = f"postgresql+psycopg2://{usuario}:{clave}@{host}:{puerto}/{base_datos}"

# *****--- 2. CONFIGURACIÓN DEL PIPELINE ---****

# tabla en la base de datos
TABLE_NAME = "transacciones"
# tamaño de los micro-lotes (número de filas a leer a la vez)
CHUNK_SIZE = 15

# lista de archivos para la carga inicial
initial_files = [
    r"C:\Users\hp\Documents\Prueba_Pragma\CSV_Data\2012-1.csv",
    r"C:\Users\hp\Documents\Prueba_Pragma\CSV_Data\2012-2.csv",
    r"C:\Users\hp\Documents\Prueba_Pragma\CSV_Data\2012-3.csv",
    r"C:\Users\hp\Documents\Prueba_Pragma\CSV_Data\2012-4.csv",
    r"C:\Users\hp\Documents\Prueba_Pragma\CSV_Data\2012-5.csv"
]

# archivo de validación
validation_file = [
    r"C:\Users\hp\Documents\Prueba_Pragma\validation.csv"
]


try:
    engine = create_engine(url_conexion)
    print(" Conexión a PostgreSQL establecida correctamente.")
except Exception as e:
    print(f" Error al crear el motor de conexión: {e}")
    exit()

# ***--- 3. CLASE PARA GESTIONAR ESTADÍSTICAS ---***

class StatisticsTracker:

    def __init__(self):
        self.count = 0
        self.min_price = float('inf')
        self.max_price = float('-inf')
        self.total_sum = 0.0
        self.mean_price = 0.0

    def update(self, df_chunk):
        
        if df_chunk.empty:
            return
        
        self.count += len(df_chunk)
        self.total_sum += df_chunk['price'].sum()
        self.mean_price = self.total_sum / self.count if self.count > 0 else 0
        self.min_price = min(self.min_price, df_chunk['price'].min())
        self.max_price = max(self.max_price, df_chunk['price'].max())

    def print_stats(self, title="Estadísticas en ejecución"):
        
        print(f"\n--- {title} ---")
        print(f"Total de filas cargadas: {self.count}")
        print(f"Precio promedio: {self.mean_price:.4f}")
        print(f"Precio mínimo: {self.min_price}")
        print(f"Precio máximo: {self.max_price}")
        print("--------------------------------------")


# ***--- 4. FUNCIONES DEL PIPELINE ---***************************

def setup_database():
    
    try:
        with engine.connect() as connection:
            # PostgreSQL usa SERIAL para claves primarias autoincrementales
            # y NUMERIC para datos financieros precisos.
            create_table_query = text(f"""
            DROP TABLE IF EXISTS {TABLE_NAME};
            CREATE TABLE {TABLE_NAME} (
                id SERIAL PRIMARY KEY,
                timestamp TEXT,
                price NUMERIC(10, 2),
                user_id TEXT
            );
            """)
            connection.execute(create_table_query)
            connection.commit()
        print(f" Tabla '{TABLE_NAME}' creada/limpiada en la base de datos '{base_datos}'.")
    except Exception as e:
        print(f" Error al configurar la tabla: {e}")
        exit()


def process_files(file_list, stats_tracker):
    
    print(f"\n Iniciando procesamiento de {len(file_list)} archivo(s)...")
    for csv_file in file_list:
        print(f"\n Procesando archivo: {csv_file}")
        try:
            for chunk_df in pd.read_csv(csv_file, chunksize=CHUNK_SIZE):
                chunk_df.to_sql(TABLE_NAME, engine, if_exists='append', index=False)
                stats_tracker.update(chunk_df)

            stats_tracker.print_stats(f"Estadísticas al finalizar {csv_file.split('\\')[-1]}")
        
        except FileNotFoundError:
            print(f"  Advertencia: El archivo {csv_file} no fue encontrado.")
        except Exception as e:
            print(f" Error procesando el archivo {csv_file}: {e}")


def verify_with_db_query(message):
   
    print(f"\n {message}")
    query = f"SELECT COUNT(*), AVG(price), MIN(price), MAX(price) FROM {TABLE_NAME};"
    try:
        with engine.connect() as connection:
            result_df = pd.read_sql_query(sql=text(query), con=connection)
        print("Resultados de la consulta a la BD:")
        print(result_df.to_string(index=False))
    except Exception as e:
        print(f" Error al consultar la base de datos: {e}")

# *****--- 5. EJECUCIÓN PRINCIPAL DEL RETO ---******

if __name__ == "__main__":
    
    # 1. Configurar (limpiar y crear) la tabla en la BD
    setup_database()

    # 2. Inicializar el rastreador de estadísticas
    stats = StatisticsTracker()

    # 3. Procesar la carga inicial de archivos
    process_files(initial_files, stats)
    
    # 4. Comprobar resultados de la carga inicial
    verify_with_db_query("Verificación en BD después de la carga inicial")
    
    print("\n" + "="*50 + "\n")
    
    # 5. Procesar el archivo de validación
    process_files(validation_file, stats)

    # 6. Comprobar los resultados finales
    verify_with_db_query("Verificación final en BD tras cargar archivo de validación")
    
    print("\n Validacion completada.")