from pyspark.sql import SparkSession
from pyspark.sql.functions import col, desc, avg, sum, max, countDistinct, collect_list, ntile, length
from pyspark.sql.types import StructField, StructType, StringType, IntegerType
from pyspark.sql.window import Window

spark = SparkSession.builder.appName('sort_search').master('local').getOrCreate()
sc = spark.sparkContext

df = spark.read.format('csv').option('header', 'true').load('input_data/customers.csv')
df.show()

## Fileter a column based on a condition
df.filter(col('CUSTOMERID') < 10).show()
## filter by gibing value of specific column
df.where(col('COUNTRY') == 'USA').show()
##Filter based on an IN list
df.where(col('CUSTOMERID').isin([2,3,4])).show()
##Filter based on an NOT IN list
df.where(~col('CUSTOMERID').isin([1,2,3,4,5])).show()
## Get Dataframe rows that match a substring
df.where(col('CUSTOMERNAME').contains('of')).show()
## Get dataframe rows that matching pattern
df.where(col('CUSTOMERNAME').like('Land%')).show()
## Filter based on a column length
df.where(length(col('CUSTOMERNAME')) < 20).show()
## Multiple filter conditions
df.filter((col('CUSTOMERID').isin([1,2,3,4,5,6,7])) & (length(col('CUSTOMERNAME')) < 20)).show()

#-------------------------------------------

## Sort the dataframe by a column
df.orderBy(col('CITY')).show()
df.orderBy(col('CITY').desc()).show()

## take first n rows of a column
df.limit(5).show()

##Get distinct values of a column
df.select(df.CITY).distinct().show()

## remove Duplicates
df.dropDuplicates(['COUNTRY']).show()

## Grouping a dataframe
##without sorting
df.groupby(col('COUNTRY')).count().show()
##with sorting
df.groupBy(col('COUNTRY')).count().orderBy(desc('count')).show()

## Filter groups based on an aggregate value, equivalent to SQL HAVING clause
df.groupBy(col('COUNTRY')).count().orderBy(desc('count')).filter(col('count') > 10).show()

## GroupBy multiple columns

df.groupBy(['CITY', 'COUNTRY']).count().orderBy(desc('count')).show()

##------------------------------------------------------------
## df for performing aggregate functions
## large data needed

data =   [
    ('Akhila', 'USA', 1000),
    ('Chandu', 'USA', 2000),
    ('Muni', 'India', 3000),
    ('Akhila', 'USA', 4000),
    ('Chandu', 'USA', 5000),
    ('Muni', 'India', 6000),
    ('Akhila', 'USA', 7000),
    ('Chandu', 'USA', 8000),
    ('Muni', 'India', 9000),
    ('Akhila', 'USA', 10000),
    ('Chandu', 'USA', 11000),
    ('Muni', 'India', 12000)
]
schema = StructType([
    StructField('name', StringType(), True),
    StructField('country', StringType(), True),
    StructField('salary', IntegerType(), True),
])
df = spark.createDataFrame(data=data, schema=schema)
df.printSchema()
df.show()
df.groupBy("country").agg(avg("salary").alias("sum_salary")).orderBy(desc("sum_salary")).show()

## Filter groups based on an aggregate value, equivalent to SQL HAVING clause
(df.groupBy('country')
 .agg(sum('salary').alias("sum_salary"))
 .filter(col('sum_salary') >= 40000).show())

## GroupBy multiple columns
(df.groupBy(['name', 'country'])
 .agg(avg('salary').alias('avg_salary'))
 .orderBy(desc('avg_salary')).show())

## select max of a column
df.select(max(col('salary')).alias('max_salary')).show()

## Sum a list of columns
expr = {x: "sum" for x in ('country', 'salary')}
df.agg(expr).show()

## Count unique values in a column after grouping
df.groupBy('country').agg(countDistinct('salary')).show()

##GroupBy and the filter on the count
df.groupBy('country').count().filter(col('count')>=2).show()

## Group key/values into a list
df.groupBy('country').agg(collect_list(col('salary'))).show(truncate=False)

## Compute global percentiles
w = Window().orderBy(col('country').desc())
df.withColumn('ntile4', ntile(4).over(w)).show()

## Compute percentiles within a partition
w = Window().partitionBy('country').orderBy(col('country').desc())
df.withColumn('ntile4', ntile(4).over(w)).show()

## Compute percentiles after aggregating
grouped = df.groupBy('country').count()
w = Window().partitionBy('country').orderBy(col('country').desc())
grouped.withColumn('ntile4', ntile(4).over(w)).show()