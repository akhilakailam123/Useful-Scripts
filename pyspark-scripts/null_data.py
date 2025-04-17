from pyspark.sql import SparkSession
from pyspark.sql.functions import col, coalesce, lit, avg

spark = SparkSession.builder.master('local').appName('Null-data-handling').getOrCreate()

# Data with NULL Values
data = [
    ('Akhila', None, 3000),
    ('Chandu', 'M', 4000),
    ('Sai', None, 4000),
    ('Sai', 'M', 4000),
    ('Sai', None, None)
]
schema = ['Name', 'Gender', 'Salary']
df = spark.createDataFrame(data, schema)
df.printSchema()
df.show()

## Filter the rows with not null values of gender
df.filter(col('Gender').isNotNull()).show()

## Replace nulls or fill the Gaps: I some cases it is useful to fill the nulls with some other values
df.na.fill({'Gender':'', 'Salary': 0 }).show()

## Use coalesce: use this function to replace the null values in a column
df.withColumn('Salary', coalesce(df['Salary'], lit(0))).show()

## Aggregating with Nulls
avg_salary = df.select(avg(df['Salary'])).collect()[0][0]
print(avg_salary)

df2 = spark.createDataFrame([
    (10, 80, 'Alice'),
    (5, None, 'Bob'),
    (None, None, 'Tom'),
    (None, None, None),
], ['Age', 'height', 'name'])
df2.show()

## Dropping rows with null Values
## You can drop rows where specific column contains null values using subset parameter
df2.na.drop(subset='Age').show()

## Drops rows where any column is NULL: ANY
df2.na.drop(how= "any").show()

## Drops rows where all the Columns are NULL
df2.na.drop(how="all").show()
