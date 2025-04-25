import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.master('local').appName('rdd').getOrCreate()

# data = [1,2,3,1,2,3,4,4,5,5,6,6,6,7,8,9,0]
#
# ## Create an RDD from parallelize
# rdd = spark.sparkContext.parallelize(data)
#
# print(rdd.collect())
#
# ## create rdd from loading a text file
# print(spark.sparkContext.textFile('input_data/data.txt').collect())
# ## It returns file path as key name and file data as value
# print(spark.sparkContext.wholeTextFiles('input_data/data.txt').collect())
# ## Create empty RDD
# print(spark.sparkContext.emptyRDD().collect())
#
# print(f"Num of partitions RDD split into: {rdd.getNumPartitions()}")
# ## We can also set the partitions manually as below
# rdd2 = spark.sparkContext.parallelize(data, 2)
# print(rdd2.collect())
# print(f"no.of partitions: {rdd2.getNumPartitions()}")
#
# rdd2 = rdd2.repartition(1)
# print(f"No.of partitions after repartition: {rdd2.getNumPartitions()}")

## RDD Transformations
# Transformations are lazy operations instead of updating an existing rdd, they return a new RDD
# 1.flatmap()

rdd3 = spark.sparkContext.textFile('input_data/data.txt')
print(rdd3.collect())

## flatmap():flattens all the data in rdd by applying the function
flatmap_rdd = rdd3.flatMap(lambda x:x.split(" "))
print(flatmap_rdd.collect())

## map(): returns all the elements of the array by applying a function
# print(rdd3.map(lambda x:x.split(" ")).collect())
map_rdd = flatmap_rdd.map(lambda x:(x,1))
print(map_rdd.collect())

##reduceBykey(): This combines the values associated to each key based on the function provided
## here the sum will combines the count of the each word
reduce_rdd = map_rdd.reduceByKey(lambda a, b: a + b)
print(reduce_rdd.collect())

## sortByKey(): Sorts the rdd based on the key value
sort_rdd = reduce_rdd.map(lambda x:(x[1],x[0])).sortByKey()
print(sort_rdd.collect())

## RDD Actions
## count(): returns the count of elements in rdd
print(f"Count of elements in RDD: {sort_rdd.count()}")

## first(): Returns the first record of the RDD
first_record = sort_rdd.first()
print(f"key: {first_record[0]}, Value: {first_record[1]}")

## max(): Returns the max record
print(f"Max record: {sort_rdd.max()}")

## reduce(): Reduces the record to single
print(sort_rdd.reduce(lambda a,b: (a[0]+b[0],a[1])))

## take(): Only return given 3 records from the
print(sort_rdd.take(3))

df_persist = sort_rdd.persist(pyspark.StorageLevel.MEMORY_ONLY)
print(df_persist.collect())

## converting dataframe from rdd
dffromrdd = sort_rdd.toDF()
dffromrdd.show()
# with column names
sort_rdd.toDF(["col1","col2"]).show()
## Convert dataframe to rdd using createdataframe
rddfromdf = spark.createDataFrame(sort_rdd)
print(rddfromdf.collect())