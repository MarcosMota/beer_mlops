import argparse
import logging
import pathlib

import boto3
import pandas as pd
from pyathena import connect
import s3fs

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
BASE_DIR = "/opt/ml/data"


def colect_sample(project_name: str, bucket_cleaned: str) -> pd.DataFrame:
    conn = connect(s3_staging_dir=f's3://{bucket_cleaned}', region_name='us-east-1')

    logger.info(f"Obtendo dados da tabela {project_name}-table do banco de dados {project_name}-db")
    df = pd.read_sql(f'SELECT * FROM "{project_name}-db"."{project_name}-table" limit 1000;', conn)
    return df


def data_wrangling(project_name: str, bucket_cleaned: str):
    pathlib.Path(f"{BASE_DIR}").mkdir(parents=True, exist_ok=True)
    df = colect_sample(project_name=project_name, bucket_cleaned=bucket_cleaned)

    logger.info(f"Salvando dataset em {BASE_DIR}")
    df.to_csv(f"{BASE_DIR}/dataset.cs", header=False, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_name", type=str, required=True)
    parser.add_argument("--bucket_cleaned", type=str, required=True)

    args = parser.parse_args()

    logger.debug("Iniciando Data Wrangling.")
    data_wrangling(project_name=args.project_name, bucket_cleaned=args.bucket_cleaned)
    logger.debug("Data Wrangling Finalizado.")
