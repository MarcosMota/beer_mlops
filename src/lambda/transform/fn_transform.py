import base64
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    output = []
    logger.info('Iniciando leitura dos eventos')
    logger.info(f"Quantidade de eventos - {len(event['records'])}")
    for record in event['records']:
        payload = json.loads(base64.b64decode(record['data']))
        logger.info(payload)
        payload_cleaned = {
            "id": payload["id"],
            "name": payload["name"],
            "abv": payload["abv"],
            "ibu": payload["ibu"],
            "target_fg": payload["target_fg"],
            "target_og": payload["target_og"],
            "ebc": payload["ebc"],
            "srm": payload["srm"],
            "ph": payload["ph"]
        }
        
        logger.info("payload transformado")
        logger.info(payload_cleaned)

        output_record = {
            "recordId": record['recordId'],
            "result": "Ok",
            "data": base64.b64encode(json.dumps(payload_cleaned).encode('utf-8')).decode('utf-8')
        }

        logger.info('Adicionando ouputs')
        logger.info(output_record)
        output.append(output_record)

    logger.info('Retornando registros mapeados')
    return {'records': output}
