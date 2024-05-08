FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \

WORKDIR /app

ADD . /app

COPY ./requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV S3_BUCKET_NAME=your-s3-bucket-name
ENV SQS_QUEUE_URL=https://sqs.aws-region.amazonaws.com/your-account-id/file-queue
ENV AWS_DEFAULT_REGION=us-east-1

EXPOSE 5000

CMD ["python", "process_service.py"]
