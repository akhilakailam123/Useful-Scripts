from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

spark = SparkSession.builder.master('local').appName('joins').getOrCreate()

## Join two DataFrames by column name
customers_data = [
    (1, "Alice", "New York"),
    (2, "Bob", "Los Angeles"),
    (3, "Charlie", "Chicago"),
    (4, "David", "Houston"),
    (5, "Eva", "Phoenix"),
    (6, "Frank", "New York"),
    (7, "Grace", "Chicago"),
    (8, "Hannah", "Phoenix"),
    (9, "Ian", "Los Angeles"),
    (10, "Jane", "Houston")
]
customers_schema = StructType([
    StructField("customer_id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("city", StringType(), True)
])
customers_df = spark.createDataFrame(data=customers_data, schema=customers_schema)
customers_df.show()

orders_data = [
    (101, 1, "Laptop", 1200.50),
    (102, 2, "Phone", 800.00),
    (103, 2, "Tablet", 300.25),
    (104, 3, "Monitor", 220.40),
    (105, 6, "Keyboard", 75.00),
    (106, 7, "Laptop", 1100.99),
    (107, 8, "Phone", 650.75),
    (108, 10, "Monitor", 199.99),
    (109, 11, "Tablet", 400.00),
    (110, 12, "Laptop", 1450.00)
]
# Schema for orders
orders_schema = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("product", StringType(), True),
    StructField("amount", DoubleType(), True)
])
orders_df = spark.createDataFrame(data=orders_data, schema=orders_schema)
orders_df.show()
## Default INNER JOIN: gives all the common rows in both dfs
customers_df.join(orders_df, 'customer_id').show()
## join dataframes with an expression
customers_df.join(orders_df, customers_df.customer_id == orders_df.customer_id).show()

## left_join: give all the rows from df1 and matchings rows
customers_df.join(orders_df, 'customer_id', 'left').show()
## right: gives all the rows in df2 and the matching rows
customers_df.join(orders_df, 'customer_id', 'right').show()
## left_anti: Rows that are only in df1
customers_df.join(orders_df, 'customer_id', 'left_anti').show()
## left_semi:
customers_df.join(orders_df, 'customer_id', 'left_semi').show()
## All the rows from both the dataframes
customers_df.join(orders_df, 'customer_id', 'full').show()
## cross join
customers_df.crossJoin(orders_df).show()

## concatenate two dataframes
df1 = spark.createDataFrame([(1, 'A'), (2, 'B')], ['id', 'value'])
df2 = spark.createDataFrame([(3, 'C'), (4, 'D')], ['id', 'value'])
df1.union(df2).show()