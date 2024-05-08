import io
import os
import json
import boto3
import pandas as pd
from sqlalchemy import create_engine

from shared.database import db_session
from shared.models import FileData, Base

s3 = boto3.client('s3')
sqs = boto3.client('sqs')

S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
SQS_QUEUE_URL = os.environ.get('SQS_QUEUE_URL')
DATABASE_URL = os.environ.get('DATABASE_URL')

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)


def process_message(message):
    file_key = message['file_key']

    try:
        file_obj = s3.get_object(Bucket=S3_BUCKET_NAME, Key=file_key)
        file_content = file_obj['Body'].read().decode('utf-8')

        df = pd.read_csv(io.StringIO(file_content))
        data = df.to_dict(orient='records')

        with db_session(DATABASE_URL) as session:
            for row in data:
                file_data = FileData(**row)
                session.add(file_data)

        s3.delete_object(Bucket=S3_BUCKET_NAME, Key=file_key)
        sqs.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=message['ReceiptHandle'])

    except Exception as e:
        print(f'Error processing file {file_key}: {e}')


def main():
    while True:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20
        )

        if 'Messages' in response:
            for message in response['Messages']:
                process_message({
                    'file_key': json.loads(message['Body'])['file_key'],
                    'ReceiptHandle': message['ReceiptHandle']
                })


if __name__ == '__main__':
    main()
