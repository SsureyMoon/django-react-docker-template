import boto3
from django.conf import settings
QUEUE_NAME = 'test-queue'

def get_sqs_client():
    sqs = boto3.resource('sqs',
                         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                         region_name=settings.SQS_AWS_REGION)
    return sqs.get_queue_by_name(QueueName=settings.SQS_NAME)

