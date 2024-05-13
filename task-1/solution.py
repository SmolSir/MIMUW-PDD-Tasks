from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json

# GROUP_DEFINITION_PATH = "data/group_definition.json"
GROUP_DEFINITION_PATH = "data/test.json"

GROUP_DEFINITION_SCHEMA = StructType([
    StructField("group", StringType(), False),
    StructField("protein_list", ArrayType(StringType(), False), False)
])

def printSparkDetails(spark: SparkSession):
    print("Details of SparkContext:")
    print(f"App Name : {spark.sparkContext.appName}")
    print(f"Master : {spark.sparkContext.master}")

def loadDataFrameGroupDefinition():
    with open(GROUP_DEFINITION_PATH) as group_definitions_file:
        return spark.createDataFrame(
            json.load(group_definitions_file).items(),
            GROUP_DEFINITION_SCHEMA
        )

###########
#   RUN   #
###########
spark = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("mySession") \
    .getOrCreate()

printSparkDetails(spark)

df_group_definition = loadDataFrameGroupDefinition()

df_group_definition.printSchema()
df_group_definition.show()
