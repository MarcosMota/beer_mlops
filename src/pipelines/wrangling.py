if __name__ == "__main__":
    logger.debug("Iniciando Data Wrangling.")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_name", type=str, required=True)
    parser.add_argument("--bucket_cleaned", type=str, required=True)
    parser.add_argument("--bucket_dataset", type=str, required=True)
    
    args = parser.parse_args()
    project_name = args.project_name
    bucket_cleaned = args.bucket_cleaned
    bucket_dataset = args.bucket_dataset
    
    pathlib.Path(f"{BASE_DIR}/data").mkdir(parents=True, exist_ok=True)
    
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=f'{bucket_dataset}')

    conn = connect(s3_staging_dir=f's3://{bucket_cleaned}', region_name='us-east-1')
    
    logger.info(f"Obtendo dados da tabela {project_name}-table do banco de dados {project_name}-db")
    df = pd.read_sql(f'SELECT * FROM "{project_name}-db"."{project_name}-table" limit 1000;', conn)

    s3f = s3fs.S3FileSystem(anon=False)

    logger.info(f"Salvando dataset")
    with s3f.open(f'{bucket_dataset}/dataset.csv', 'w') as f:
        df.to_csv(f)
        
    logger.debug("Finalizando Data Wrangling.")