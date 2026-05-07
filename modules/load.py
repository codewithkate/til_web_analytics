import os
import boto3
import logging
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

def upload_to_s3(access_key, secret_key, region, bucket, local_file_location, aws_object_destination):
    """
    This loads a single local file into an S3 destination.

    Requirements:
        - Run personalize.py
        - Run commands to do the following:
            - create bucket
            - create policy
            - create user
            - create access key
        - Record outputs in a .env file

    Args:
        access_key (str): _description_
        secret_key (str): _description_
        region (str): _description_
        bucket (str): _description_
        local_file_location (Path object): _description_.
        aws_object_destination (str): _description_.
    
    Return:
        bool: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if aws_object_destination is None:
        aws_object_destination = os.path.basename(local_file_location)

    # Upload the file
    s3_client = boto3.client(
        service_name='s3',
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    try:
        response = s3_client.upload_file(local_file_location, bucket, aws_object_destination)
        logger.info(f'{aws_object_destination} uploaded to S3')
    except Exception as e:
        logger.error(e)
        return False
    return True

