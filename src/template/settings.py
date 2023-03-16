from enum import Enum
from functools import lru_cache

from pydantic import BaseSettings

from template.logger import logger


class Environment(Enum):
    TEST = "TEST"
    DEV = "DEV"
    PROD = "PROD"


class Settings(BaseSettings):
    APP_NAME: str = "Template"
    ENV: Environment = Environment.DEV
    DEBUG: bool = False
    AWS_REGION: str = "eu-central-1"
    SPARK_CLUSTER: str = ""
    SSM_SPARK_CLUSTER = "/Template/spark_cluster_address"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    """Get the required settings from AWS SSM Parameter Store."""
    s = Settings()

    def fetch_config_ssm():
        import botocore.session
        from botocore.client import BaseClient as SSMClient
        from botocore.exceptions import ClientError

        def get_parameter_store_value(client: SSMClient, parameter_name) -> str:
            result = client.get_parameter(Name=parameter_name, WithDecryption=True)
            return result["Parameter"]["Value"]

        try:
            session = botocore.session.get_session()
            client = session.create_client("ssm", region_name="eu-central-1")

            spark_cluster_ip = get_parameter_store_value(client, s.SSM_SPARK_CLUSTER)

            return {
                "SPARK_CLUSTER": spark_cluster_ip,
            }
        except ClientError as err:
            logger.error(f"Error fetching config from SSM: {err}.")
        except Exception as err:
            logger.error(f"Error: {err}.")

        return {}

    paramss = fetch_config_ssm()
    s.SPARK_CLUSTER = paramss.get("SPARK_CLUSTER", "spark://spark-master:7077")

    return s


settings = get_settings()
