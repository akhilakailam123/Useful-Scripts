from pyspark.sql import SparkSession

spark = SparkSession.builder.master('local').appName('rdd').getOrCreate()

data = [1,2,3,1,2,3,4,4,5,5,6,6,6,7,8,9,0]

## Create an RDD from parallelize
rdd = spark.sparkContext.parallelize(data)

print(rdd.collect())

## create rdd from loading a text file
print(spark.sparkContext.textFile('input_data/data.txt').collect())
## It returns file path as key name and file data as value
print(spark.sparkContext.wholeTextFiles('input_data/data.txt').collect())
## Create empty RDD
print(spark.sparkContext.emptyRDD().collect())

print(f"Num of partitions RDD split into: {rdd.getNumPartitions()}")
## We can also set the partitions manually as below
rdd2 = spark.sparkContext.parallelize(data, 2)
print(rdd2.collect())
print(f"no.of partitions: {rdd2.getNumPartitions()}")

rdd2 = rdd2.repartition(1)
print(f"No.of partitions after repartition: {rdd2.getNumPartitions()}")