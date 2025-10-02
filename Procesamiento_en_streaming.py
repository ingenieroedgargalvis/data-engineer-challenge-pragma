import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, min, max, count

# ********-------------  CONFIGURACIÓN DE JAVA Y HADOOP --------------*****************
os.environ["JAVA_HOME"] = r"C:\Program Files\Eclipse Adoptium\jdk-17.0.16.8-hotspot"
os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["hadoop.home.dir"] = r"C:\hadoop"
os.environ["PATH"] += os.pathsep + r"C:\hadoop\bin"

# **************-------------- CREAR SPARKSESSION ---------***************
spark = SparkSession.builder \
    .appName("PragmaDataPipelineStreaming") \
    .config("spark.hadoop.fs.file.impl.disable.cache", "true") \
    .config("spark.driver.extraJavaOptions", "-Djava.library.path=C:/hadoop/bin") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print("✅ SparkSession Streaming iniciada correctamente")

# ***********------- CONFIG POSTGRES ----------------**************
url = "jdbc:postgresql://localhost:5432/PRAGMA"
usuario = "postgres"
clave = "MiClaveSegura2025"
tabla = "transacciones_stream"

db_props = {
    "user": usuario,
    "password": clave,
    "driver": "org.postgresql.Driver"
}

# ************--------- FUENTE DE STREAMING *----
# Carpeta donde se copiarán los CSV uno a uno
input_dir = r"C:\Users\hp\Documents\Prueba_Pragma\CSV_Data\stream_input"

# Definir schema para evitar inferSchema en streaming
schema = "timestamp STRING, price DOUBLE, user_id STRING"

# Leer en streaming (espera a que aparezcan nuevos archivos CSV en input_dir)
df_stream = spark.readStream \
    .option("header", True) \
    .schema(schema) \
    .csv(input_dir)

# ***********---- ESTADÍSTICAS INCREMENTALES ---****************
stats = df_stream.groupBy().agg(
    count("*").alias("total_filas"),
    avg(col("price")).alias("precio_promedio"),
    min(col("price")).alias("precio_minimo"),
    max(col("price")).alias("precio_maximo")
)

# *****************------------  ESCRITURA EN POSTGRES ------------***************
def write_to_postgres(batch_df, batch_id):
    batch_df.write.jdbc(url=url, table=tabla, mode="append", properties=db_props)

# *****************-------- SALIDA A CONSOLA + POSTGRES ----------------********************
query = stats.writeStream \
    .outputMode("complete") \
    .foreachBatch(write_to_postgres) \
    .format("console") \
    .option("truncate", False) \
    .start()

print(" Esperando archivos CSV en la carpeta:", input_dir)

query.awaitTermination()
