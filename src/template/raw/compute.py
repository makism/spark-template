from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql import functions as F

from template.raw.schemas import SCHEMA_RAW, SCHEMA_EXPECTED_FILES
from template.utils import spark_session
from template.logger import logger


def check_input_sources(
    df: DataFrame, session: SparkSession, expected_sources: list[str]
) -> DataFrame:
    """Check that all input files are from the same source."""
    files_df = df.withColumn(
        "_source_filename", F.element_at(F.split("_source_filename", "/"), -1)
    )

    rows_per_file_df = df.groupby("_source_filename").count()
    logger.info(rows_per_file_df.toPandas().to_dict("records"))

    expected_df = spark.createDataFrame(
        data=[{"expected_filename": file} for file in expected_sources],
        schema=SCHEMA_EXPECTED_FILES,
    )

    res = expected_df.join(
        files_df,
        on=[expected_df.expected_filename == files_df._source_filename],
        how="left",
    )

    if res.count() != len(expected_sources):
        logger.info("There are missing files in the input source.")


if __name__ == "__main__":
    spark = spark_session()

    raw_df = spark.read.option("recursiveFileLookup", "true").json("/data/raw/*.json")

    raw_df = raw_df.withColumn("_source_filename", F.input_file_name())

    check_input_sources(
        raw_df,
        session=spark,
        expected_sources=[
            "input-file-000.json",
            "input-file-001.json",
            "input-file-002.json",
        ],
    )

    (
        raw_df.coalesce(1).write.parquet(
            "/datalake/raw/",
            mode="overwrite",
        )
    )
