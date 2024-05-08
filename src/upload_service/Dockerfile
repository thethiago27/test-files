FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV S3_BUCKET_NAME=your-s3-bucket-name
ENV SQS_QUEUE_URL=https://sqs.aws-region.amazonaws.com/your-account-id/file-queue

EXPOSE 5000

CMD ["python", "upload_service.py"]
