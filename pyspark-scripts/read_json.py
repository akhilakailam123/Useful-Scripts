from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType, BooleanType

spark = SparkSession.builder.master('local').appName('json_data').getOrCreate()

schema = StructType([
    StructField('user', StructType([
        StructField('id', IntegerType(), True),
        StructField('name', StructType([
            StructField("first", StringType(), True),
            StructField('last', StringType(), True)
        ])),
        StructField("contact", StructType([
            StructField("email", StringType(), True),
            StructField("phones", ArrayType(StructType([
                StructField("type", StringType(), True),
                StructField("number", StringType(), True)
            ])))
        ])),
        StructField("roles", ArrayType(StringType()), True),
        StructField("active", BooleanType(), True)
    ])),
    StructField("meta", StructType([
        StructField("created_at", StringType(), True),
        StructField("updated_at", StringType(), True)
    ]))
])
dataframe = spark.read.format('json').option('multiline', True).load('input_data/data.json')
dataframe.show(truncate=False)

## flattening the structure:
flat_df = dataframe.select(
    col("user.id").alias("user_id"),
    col("user.name.first").alias("firstname"),
    col("user.name.last").alias("lastname"),
    col("user.contact.email").alias("email"),
    explode(col("user.contact.phones")).alias('phone'),
    explode(col("user.roles")).alias('role'),
    col("user.active").alias('is_active'),
    col("meta.created_at"),
    col("meta.updated_at")
)
# now select necessary columns
flat_df.select(
    "user_id", "firstname", "lastname", "email",
    col("phone.type").alias('phone_type'),
    col("phone.number").alias('phone_number'),
    "role", "is_active", "created_at", "updated_at"
).show()


## Using python function: Flattening the Json data
def flatten_data(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

data = {
    "user": {
        "id": 123,
        "name": {
            "first": "John",
            "last": "Doe"
        },
        "contact": {
            "email": "john.doe@example.com",
            "phones": [
                {
                    "type": "home",
                    "number": "123-456-7890"
                },
                {
                    "type": "work",
                    "number": "987-654-3210"
                }
            ]
        },
        "roles": ["admin", "editor"],
        "active": True
    },
    "meta": {
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2025-01-01T12:00:00Z"
    }
}

flat_data = flatten_data(data)
print(flat_data)
