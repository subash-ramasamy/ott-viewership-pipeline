"""
Script. : Load Clean parquet Files to BigQuery
Purpose : Upload all 3 cleaned datasets to Big Query for SQL transformnation queries
"""

from google.cloud import bigquery
import pandas as pd
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────
PROJECT_ID  = "ott-viewership-pipeline"    # replace with yours
DATASET_ID  = "ott_viewership"
TABLES = {
    "barc_ratings":       "data/parquet/barc_clean.parquet",
    "ott_events":         "data/parquet/ott_clean.parquet",
    "social_engagement":  "data/parquet/social_clean.parquet",
}

def load_table(client,df,table_id):
    job_config = bigquery.LoadJobConfig(
        write_disposition = "WRITE_TRUNCATE"
    )
    job = client.load_table_from_dataframe(df, table_id,job_config = job_config)
    job.result(
        logger.info(f"loaded{len(df)} rows -> {table_id}")
    )

def main():
    logger.info("Big Query Loadinfg Started")
    client = bigquery.Client(project =PROJECT_ID)

    for table_name, parquet_path in TABLES.items():
        try:
            df = pd.read_parquet(parquet_path)
            table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
            load_table(client,df,table_id)
        except FileNotFoundError:
            logger.error(f"File not found:{parquet_path}")
            raise
    
    logger.info("All tables loaded to Big Query")

if __name__ == "__main__":
    main()
