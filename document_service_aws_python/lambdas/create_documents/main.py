import json
import os
import uuid
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = os.environ.get('DOCUMENT_TABLE_NAME')
REGION = os.environ.get('REGION')


def main(event, context):
    logger.info(event)
    logger.info(context)
    random_value = str(uuid.uuid4().hex)
    print(f'Random value is {random_value}')

    dynamodb = boto3.resource('dynamodb', region_name=REGION)

    table = dynamodb.Table(TABLE_NAME)
    response = table.put_item(
        Item={
            'ID': random_value
        }
    )
    print("PutItem succeeded:")
    print(json.dumps(response, indent=2))
