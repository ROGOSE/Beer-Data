from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, collect_list, desc, round as spark_round

# Crear una sesión de Spark
sc = SparkSession.builder.appName("Topear_ABV").getOrCreate()

# Cargar el archivo JSON en un DataFrame
path = "beeradvocate_note.json"
df = sc.read.json(path)

df = df.withColumn("review/note", col("review/note").cast("float"))

# Calcular la nota media por cerveza
df_notas_medias = df.groupBy("beer/name", "beer/ABV").agg(spark_round(avg("review/note"), 2).alias("beers_average"))

# Agrupar por "beer/ABV" y obtener una lista de "beer/name" ordenadas por nota media
df_agrupado = df_notas_medias.groupBy("beer/ABV") \
                .agg(collect_list("beer/name").alias("beer_names"), spark_round(avg("beers_average"), 2).alias("ABV_average")) \
                .orderBy(desc("ABV_average"))
                

df_agrupado.show(truncate=False)

sc.stop()
