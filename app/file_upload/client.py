# app/utils/r2_client.py

import logging

from django.conf import settings

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

LOGGER_CLIENT_R2 = '[R2-CLIENT]'

class R2Client:
    def __init__(self):
        self.client = boto3.client('s3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4'),
            region_name=settings.AWS_S3_REGION_NAME
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        self.public_url = "https://{}".format(settings.AWS_S3_CUSTOM_DOMAIN)

    def upload_file(self, file_obj, file_name):
        try:
               # Add CORS headers in the metadata
            extra_args = {
                'Metadata': {
                    'x-amz-acl': 'public-read'
                },
                'ContentType': file_obj.content_type,  # Set proper content type
                'ACL': 'public-read',
                # Add CORS headers
                'CacheControl': 'max-age=86400',
                'ContentDisposition': f'inline; filename="{file_name}"'
            }
            self.client.upload_fileobj(
                file_obj,
                self.bucket_name,
                file_name,
                ExtraArgs=extra_args
            )
            # Custom domain already points to the bucket, so don't include bucket name in URL
            return "{}/{}".format(self.public_url, file_name)
        except ClientError as e:
            # You might want to log this error
            logger.error("{}: An error occurred: {}".format(LOGGER_CLIENT_R2, e))
            return None

    def delete_file(self, file_name):
        try:
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=file_name
            )
            return True
        except ClientError as e:
            # You might want to log this error
            logger.error("{}: An error occurred: {}".format(LOGGER_CLIENT_R2, e))
            return False

    