from pyspark.sql import functions as F
from pyspark.sql import types as T
from pyspark.sql.dataframe import DataFrame


from template.utils import spark_session, iso8601_to_minutes


def preprocess_columns(df: DataFrame) -> DataFrame:
    """Apply common preprocessing steps to input DataFrame."""
    clean_df = df.withColumn("name", F.lower(F.col("name")))
    return clean_df


def convert_iso8601_to_minutes(
    df: DataFrame, target_cols: list[str] = ["time", "previous_time"]
) -> DataFrame:
    """Convert ISO8601 duration strings to minutes."""
    udf_iso8601_to_minutes = F.udf(iso8601_to_minutes, T.IntegerType())

    for col in target_cols:
        new_col = col

        df = df.withColumn(
            new_col,
            F.when(
                F.length(F.col(col)) > 2, udf_iso8601_to_minutes(F.col(col))
            ).otherwise(-1),
        )

    return df


if __name__ == "__main__":
    spark = spark_session()

    input_df = spark.read.parquet("/datalake/raw/")

    clean_df = preprocess_columns(input_df)
    clean_df = convert_iso8601_to_minutes(clean_df)

    (
        clean_df.coalesce(1).write.parquet(
            "/datalake/clean/",
            mode="overwrite",
        )
    )
