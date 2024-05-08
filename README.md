# FILE_SERVICE

FILE_SERVICE is a microservice designed to handle the upload and processing of CSV files. It follows a serverless architecture pattern, leveraging AWS services such as AWS Lambda, Amazon S3, Amazon SQS, and Amazon RDS (PostgreSQL).

## Architecture

The microservice consists of two main components:

1. **Upload Service**: A Flask application that handles file uploads to an S3 bucket and sends a message to an SQS queue with the file key.
2. **Process Service**: A Python application that listens to the SQS queue, processes the CSV file data, and persists it in the database.

The architecture is designed to be resilient, scalable, and fault-tolerant. If a service fails during processing, the message remains in the SQS queue, and the process can be retried later. Additionally, the use of SQS guarantees that messages are processed at least once, preventing data duplication.

## Prerequisites

Before running the FILE_SERVICE microservice, ensure that you have the following prerequisites installed:

- Python 3.7 or later
- Docker
- Docker Compose (for local development)
- AWS CLI (for production deployment)

## Local Development

To run the microservice locally, follow these steps:

1. Clone the repository:

2. Create a `.env` file in the project root directory and set the required environment variables:

``
S3_BUCKET_NAME=local-bucket
SQS_QUEUE_URL=http://localhost:9324/queue/file-queue
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/file_service
``
3. Start the services using Docker Compose:
docker-compose -f infrastructure/local/docker-compose.yml up

This will start the required services (PostgreSQL, LocalStack for S3 and SQS, and the Upload and Process services).

4. Upload a CSV file to the local S3 bucket using the AWS CLI or a tool like Cyberduck.

5. The Process Service will automatically pick up the file from the SQS queue and process the data.

## Production Deployment

To deploy the FILE_SERVICE microservice to a production environment (AWS), follow these steps:

1. Create the required AWS resources (S3 bucket, SQS queue, and RDS instance) using the provided CloudFormation templates:

``
aws cloudformation create-stack --stack-name file-service-s3-bucket --template-body file://infrastructure/prod/cloudformation/s3.yaml
aws cloudformation create-stack --stack-name file-service-sqs-queue --template-body file://infrastructure/prod/cloudformation/sqs.yaml
aws cloudformation create-stack --stack-name file-service-rds-instance --template-body file://infrastructure/prod/cloudformation/rds.yaml
``


2. Build and push the Docker images for the Upload and Process services to a Docker registry (e.g., Docker Hub, Amazon ECR).

3. Deploy the services to an EKS cluster using the provided Kubernetes manifests:

kubectl apply -f infrastructure/prod/kubernetes/


