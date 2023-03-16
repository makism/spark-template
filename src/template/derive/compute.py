from pyspark.sql import functions as F
from pyspark.sql import types as T
from pyspark.sql.dataframe import DataFrame


from template.utils import spark_session


def derive_columns(df: DataFrame) -> DataFrame:
    derived_df = df.withColumn("current_time", F.col("time") + F.col("previous_time"))

    derived_df = derived_df.withColumn(
        # Add columns
    )

    return derived_df


if __name__ == "__main__":
    spark = spark_session()

    input_df = spark.read.parquet("/datalake/clean/")

    filtered_df = (
        input_df
        # More filtering here
        .distinct()
    )

    derived_df = derive_columns(filtered_df)

    # Extract metrics here

    (
        metrics_df.write.mode("overwrite")
        .options(header=True, delimiter=",")
        .csv("/datalake/derive/")
    )
