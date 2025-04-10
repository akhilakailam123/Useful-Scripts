from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType

'''MAP
Use map when you want a one-to-one transformation, 
where each input element corresponds to exactly one output element.'''

spark = SparkSession.builder.master('local').appName('map/flatmap').getOrCreate()
sc = spark.sparkContext
# create an rdd
rdd =  sc.parallelize([2,3,4])
print(rdd.collect())
print(rdd.map(lambda x: [x,x,x]).collect())

# No.of ele in i/p = No.of elements in o/p
# I/P: [2, 3, 4]
# O/P: [[2, 2, 2], [3, 3, 3], [4, 4, 4]]

'''Use flatMap when you want to perform a transformation that 
can generate zero or more output elements for each input element, 
and you want to flatten the results into a single RDD or DataFrame.
'''

print(rdd.flatMap(lambda x: [x,x,x]).collect())
# O/P: [2, 2, 2, 3, 3, 3, 4, 4, 4]

## Apply a function to each element in the RDD
data = [('1', 'Akhila'), ('2', 'Chandu'), ('3', 'muni'), ('4', 'ammu')]
schema = StructType([
    StructField("id", StringType(), True),
    StructField("name", StringType(), True)
])
df = spark.createDataFrame(data=data, schema=schema)

def map_function(row):
    if row.name == 'Akhila':
        return (row.id, row.name.upper())
    else:
        return (row.id, row.name.lower())

print(df.rdd.map(map_function).collect())
df.rdd.map(map_function).toDF().show()
print(df.rdd.flatMap(map_function).collect())
