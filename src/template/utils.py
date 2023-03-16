import re

from pyspark.sql import SparkSession


def spark_session(name: str = "Template") -> SparkSession:
    """Create (or get an existing one) a SparkSession object."""
    from template.settings import settings

    return (
        SparkSession.builder.appName("Template")
        .master(settings.SPARK_CLUSTER)
        .getOrCreate()
    )


def iso8601_to_minutes(duration: str) -> int:
    """Convert a given string that represent a time duration in ISO8601 format to minutes."""
    minutes = 0
    pattern = re.compile("^PT((?P<hours>[0-9]+)H)?((?P<minutes>[0-9]+)M)?")

    match = pattern.match(duration)
    if match:
        if match.group("hours"):
            minutes += int(match.group("hours")) * 60
        if match.group("minutes"):
            minutes += int(match.group("minutes"))

    return minutes
