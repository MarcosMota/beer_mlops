from pyathena import connect
import pandas as pd
import boto3
import s3fs


def collect_samples(project_name: str, region_name: str,
                    bucket_from: str, bucket_to: str):
    """
    Args
        :param project_name:
        :param region_name:
        :param bucket_from:
        :param bucket_to:
    Return:
    """
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=f'{bucket_to}')

    conn = connect(s3_staging_dir=f's3://{bucket_from}',
                   region_name=region_name)

    df = pd.read_sql(f'SELECT * FROM "{project_name}-db"."{project_name}-table" limit 1000;', conn)

    s3f = s3fs.S3FileSystem(anon=False)

    with s3f.open(f'{bucket_to}/dataset.csv', 'w') as f:
        df.to_csv(f)

    return f'{bucket_to}/dataset.csv'


def load_data(bucket: str, dataset_file: str, columns_names: list, columns_dtype: dict) -> pd.DataFrame:
    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket=bucket, Key=dataset_file)
    df = pd.read_csv(response.get("Body"), names=columns_names, dtype=columns_dtype)
    return df
