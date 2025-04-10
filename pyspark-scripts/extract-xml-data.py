from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType

spark = SparkSession \
    .builder \
    .appName("Test") \
    .config("spark.jars.packages", "com.databricks:spark-xml_2.12:0.13.0") \
    .getOrCreate()

df2_schema = StructType([
    StructField("_id", StringType(), True),
    StructField("author", StringType(), True),
    StructField("title", StringType(), True),
    StructField("genre", StringType(), True),
    StructField("price", StringType(), True),
    StructField("publish_date", StringType(), True),
    StructField("description", StringType(), True),
])
df2 = (spark.read.format('xml')
       .options(rowTag='book')
       .option("attributePrefix", "_")
       .schema(df2_schema)
       .load('input_data/xml_data.xml')
       )
df2.printSchema()
df2.show()

'''Run file with spark-submit if issues occures
spark-submit --packages com.databricks:spark-xml_2.12:0.13.0 extract-xml-data.py'''