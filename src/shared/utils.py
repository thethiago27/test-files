import os
import boto3


def get_s3_client():
    return boto3.client('s3')


def get_sqs_client():
    return boto3.client('sqs')


def get_env_var(var_name):
    return os.environ.get(var_name)
