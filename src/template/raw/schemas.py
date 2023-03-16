from pyspark.sql import types as T

SCHEMA_RAW = T.StructType(
    [
        T.StructField("description", T.StringType(), True),
        T.StructField("image", T.StringType(), True),
        T.StructField("name", T.StringType(), True),
        T.StructField("url", T.StringType(), True),
    ]
)

SCHEMA_EXPECTED_FILES = T.StructType(
    [
        T.StructField("expected_filename", T.StringType(), False),
    ]
)
