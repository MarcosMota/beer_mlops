import json
import os

import boto3
import requests

REGION_NAME = os.environ['AWS_REGION']
STREAM_NAME = os.environ['PROJECT_STEAM']


def handler(event, lambda_context):
    KINESIS_CLIENT = boto3.client('kinesis', region_name=REGION_NAME)
    # Realizando o get na API para a ingestao dos dados
    response = requests.get("https://api.punkapi.com/v2/beers/random")
    data = response.json()[0]

    # Enviando os dados para o Kinesis
    put_response = KINESIS_CLIENT.put_record(
        StreamName=STREAM_NAME,
        Data=json.dumps(data),
        PartitionKey="partition_key"
    )

    return data


if __name__ == '__main__':
    handler('', '')
