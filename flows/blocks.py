from prefect_gcp import GcpCredentials, BigQueryWarehouse
from prefect_gcp.cloud_storage import GcsBucket
from prefect_dbt.cli import BigQueryTargetConfigs, DbtCliProfile
import os
from pathlib import Path


service_account_file = Path(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
credentials_block = GcpCredentials(service_account_file = service_account_file)
res = credentials_block.save("google-credentials", overwrite=True)

bucket_name = "" #insert your gcp bucket name here
bucket_block = GcsBucket(
    gcp_credentials=credentials_block,
    bucket=bucket_name,
)
bucket_block.save("gcs-bucket", overwrite=True)

BigQueryWarehouse(gcp_credentials=credentials_block).save("bq-block", overwrite=True)

target_configs = BigQueryTargetConfigs(
    schema="dbt_bus_schema", 
    project="final-385014",
    credentials=credentials_block,
)
target_configs.save("bq-block-dbt", overwrite=True)

dbt_cli_profile = DbtCliProfile(
    name="wmata_bus",
    target="dev",
    target_configs=target_configs,
)
dbt_cli_profile.save("dbt-cli-profile", overwrite=True)