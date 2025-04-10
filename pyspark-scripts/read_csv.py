from pyspark.sql import SparkSession
from pyspark.sql.functions import upper, lower, col, lit, concat, when
from pyspark.sql.types import StringType, StructField, StructType

spark = SparkSession.builder.master('local').appName('csvfile').getOrCreate()

schema = StructType([
    StructField("CUSTOMERID", StringType(), True),
    StructField("CUSTOMERNAME", StringType(), True),
    StructField("EMAIL", StringType(), True),
    StructField("CITY", StringType(), True),
    StructField("COUNTRY", StringType(), True),
    StructField("TERRITORY", StringType(), True),
    StructField("CONTACTFIRSTNAME", StringType(), True),
    StructField("CONTACTLASTNAME", StringType(), True)
])

df = (spark.read
      .format('csv')
      .option('header', 'true')
      .schema(schema)
      .load('input_data/customers.csv'))

df.printSchema()
df.show(truncate=False)

'''Data Handling Options'''

## Save a dataframe as a CSV file
df.write.mode('overwrite').csv('output_data/customers.csv', header=True)

##Save DataFrame as a dynamic partitioned table
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
df.write.mode('overwrite').partitionBy('TERRITORY').csv('output_data/csv_partitioned.csv')

## Save the csv data in a single file
df.coalesce(1).write.mode('overwrite').csv('output_data/single_file.csv', header=True)

## add a column to the dataframe
(df.withColumn('extra_column', upper(df.CITY))
 .withColumn('second_extra', lower(df.TERRITORY)).show())

## modifying exiting column
df.withColumn('CITY', concat(lit('US'), col('CITY'))).show()

## add a column with multiple conditions using when otherwise
df.withColumn('FULL_COUNTRY_NAME',
              when (col('COUNTRY') == 'USA', "United Sates")
              .when (col('COUNTRY') == 'France', "FRANCE_COUNTRY")
              .when (col('COUNTRY') == 'Norway', 'NORWAY_COUNTRY')
              .otherwise ('UNKNOWN')).show()

## concatenate columns
df.withColumn('FULL_NAME', concat(col('CONTACTFIRSTNAME'), lit('_'), col('CONTACTLASTNAME'))).show()

## drop a column
df.drop(col('TERRITORY')).show()

## Change column names
df.withColumnRenamed('CUSTOMERID', 'ID').withColumnRenamed('COUNTRY', 'Country').show()

## change all the columns at once
df.toDF(*["x"+ name for name in df.columns]).show()

# convert a column values into a list

names = df.select('CITY').rdd.flatMap(lambda x: x).collect()
print(str(names[:10]))

## Consume a DataFrame row-wise as Python dictionaries
small_df = df.limit(3)
for row in small_df.collect():
    r = row.asDict()
    print(r)

## select particular columns from dataframe
df.select(['CUSTOMERID', 'CUSTOMERNAME', 'EMAIL']).show()

# create an empty dataframe with specified schema

df_schema = StructType([
    StructField('id', StringType(), True),
    StructField('name', StringType(), True )
])

empty_df = spark.createDataFrame([], schema=df_schema)
empty_df.show()

## Create a constant dataframe
spark.createDataFrame([
    ('1', 'Akhila'),
    ('2', 'Chandu')
], schema=df_schema
).show()

## convert the datatype of a column
empty_df.withColumn('id', col('id').cast('double')).printSchema()

## get the size of the dataframe
print(f"No.of rows: {df.count()}")
print(f"No.of Columns: {len(df.columns)}")
