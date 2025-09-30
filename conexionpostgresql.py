from sqlalchemy import create_engine

usuario = "postgres"
clave = "MiClaveSegura2025"
host = "localhost"
puerto = "5432"
base_datos = "PRAGMA"

# Construir URL
url_conexion = f"postgresql+psycopg2://{usuario}:{clave}@{host}:{puerto}/{base_datos}"

try:
    engine = create_engine(url_conexion)
    conexion = engine.connect()
    print("✅ Conexión exitosa a PostgreSQL")
    conexion.close()
except Exception as e:
    print("❌ Error al conectar:", e)
