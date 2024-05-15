import pyspark.sql.functions as PySQL
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from random import randint
from typing import List
import numpy as np
import hashlib
import json
import timeit

###############
#   GLOBALS   #
###############
SHINGLE_SIZE = 5
BAND_SIZE    = 20
ROW_SIZE     = 5

TEST = False
PERF = True

# Shingles
SHINGLE_BASE = ord("Z") - ord("A") + 1

# Minhash
HASH_MOD = 1_000_000_007
PERMUTATION_COUNT = BAND_SIZE * ROW_SIZE
RAND_MAX = (2 ** 32) - 1
PERMUTATION_ARR = np.array([
    (randint(1, RAND_MAX), randint(0, RAND_MAX))
    for _ in range(PERMUTATION_COUNT)
])

# Spark
SPARK = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("mySession") \
    .getOrCreate()

# Group definition file
GROUP_DEFINITION_PATH   = "data/test.json" if TEST else "data/bruh.json" if PERF else "data/group_definition.json"
GROUP_DEFINITION_SCHEMA = StructType([
    StructField("group", StringType(), False),
    StructField("protein_list", ArrayType(StringType(), False), False)
])

# Fasta directory
FASTA_PATH   = "data/test_fasta" if TEST else "data/bruh_fasta" if PERF else "data/fasta"
FASTA_SCHEMA = StructType([
    StructField("name", StringType(), False),
    StructField("value", StringType(), False)
])

#################
#   FUNCTIONS   #
#################
def benchmark():
    with open("data/bruh_fasta/A0A1P8XQ85.json") as f:
        d = json.load(f)
        getMinhashesOfBands(d["value"])

def printSparkDetails(spark: SparkSession):
    print("Details of SparkContext:")
    print(f"App Name : {spark.sparkContext.appName}")
    print(f"Master : {spark.sparkContext.master}")

def loadDataFrameGroupDefinition():
    with open(GROUP_DEFINITION_PATH) as group_definitions_file:
        return SPARK.createDataFrame(
            json.load(group_definitions_file).items(),
            GROUP_DEFINITION_SCHEMA
        )

def loadDataFrameFasta():
    return SPARK.read.schema(FASTA_SCHEMA).json(FASTA_PATH)

def getMinhashesOfBands(value: StringType):
    def shingle_int(shingle: StringType):
        return sum(
            (ord(aminoacid) - ord("A")) * (SHINGLE_BASE ** exp)
            for exp, aminoacid in enumerate(shingle[::-1])
        )

    def batch_hash(batch: List[IntegerType]):
        batch_string = "".join(map(str, batch))
        batch_hash_sha256 = hashlib.sha256(batch_string.encode())
        return int(batch_hash_sha256.hexdigest()[:8], 16) # just the 32-bit integer

    print(value)

    shingle_char_arr = np.lib.stride_tricks.sliding_window_view(
        np.array(list(value)), window_shape=(SHINGLE_SIZE, )
    )

    print(shingle_char_arr)

    shingle_arr = np.vectorize("".join)(shingle_char_arr)

    print(shingle_arr)

    shingle_int_arr = np.vectorize(shingle_int)(shingle_arr)

    print(shingle_int_arr)

    signature_arr = np.array([
        np.min((a * shingle_int_arr + b) % HASH_MOD)
        for a, b in PERMUTATION_ARR
    ])

    print(signature_arr)

    # signature_batch_hash_list = [
    #     batch_hash(signature_list[i : i + 5])
    #     for i in range(0, PERMUTATION_COUNT, ROW_SIZE)
    # ]

    return list(signature_arr.tolist())

###########
#   RUN   #
###########
printSparkDetails(SPARK)

df_group_definition = loadDataFrameGroupDefinition()
df_fasta = loadDataFrameFasta()

udf_get_minhashes_of_bands = PySQL.udf(getMinhashesOfBands, ArrayType(IntegerType(), False))

# df_fasta = df_fasta.withColumn("minhash_band_signature_list", udf_get_minhashes_of_bands("value"))

df_group_definition.printSchema()
df_group_definition.show()

df_fasta.printSchema()
df_fasta.show()

print("smokin' time!")
print(timeit.repeat("benchmark()", "from __main__ import benchmark", repeat = 1, number = 1))
