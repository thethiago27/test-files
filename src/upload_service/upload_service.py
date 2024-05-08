import os
import json
from flask import Flask, request
from flask_swagger_ui import get_swaggerui_blueprint
import boto3

app = Flask(__name__)

s3 = boto3.client('s3')
sqs = boto3.client('sqs')

S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
SQS_QUEUE_URL = os.environ.get('SQS_QUEUE_URL')

SWAGGER_URL = '/swagger'
API_URL = '/static/docs/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'File Service API'
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400

    file = request.files['file']

    if file.filename == '':
        return {'error': 'No selected file'}, 400

    if not file.filename.endswith('.csv'):
        return {'error': 'Invalid file type'}, 400

    file_key = f"{file.filename}"
    s3.upload_fileobj(file, S3_BUCKET_NAME, file_key)

    sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=json.dumps({'file_key': file_key})
    )

    return {'message': 'File upload successful'}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
