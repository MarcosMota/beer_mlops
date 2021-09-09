import json
import os
import boto3
import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def environIsValid(aws_region: str, kinesis_steam: str) -> bool:
    if aws_region is None:
        logger.error("Variável de Ambiente AWS_REGION está vazia.")
        return False

    if kinesis_steam is None:
        logger.error("Variável de Ambiente PROJECT_STEAM está vazia.")
        return False

    return True


def handler(event, lambda_context):
    aws_region = os.environ.get('AWS_REGION', None)
    kinesis_steam = os.environ.get('PROJECT_STEAM', None)

    if environIsValid(aws_region=aws_region, kinesis_steam=kinesis_steam) is False:
        raise Exception("Variáveis AWS_REGION e PROJECT_STEAM não estão definidas")

    try:
        kinesis_client = boto3.client('kinesis', region_name=aws_region)
        response = requests.get("https://api.punkapi.com/v2/beers/random")

        if response.status_code > 200:
            raise Exception("Problemas encontrado ao obter dados da API")

        response = kinesis_client.put_record(
            StreamName=kinesis_steam,
            Data=json.dumps(response.json()[0]),
            PartitionKey="partition_key"
        )

        logger.info(f"Quantidade de eventos - {len(response.json)}")

        return response
    except Exception as ex:
        logger.error("Problemas encontrados ao executar a função de extração", ex)


if __name__ == '__main__':
    handler('', '')
