"""
Data Loading into a S3 bucket using boto3

Requirements:
    - personlize aws templates
    - run commands and record outputs in the .aws_env file
        - create bucket
        - create policy
        - create user
        - create access key
    - activate the environment
"""  
import os
import boto3
import logging
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

def configure_logs(format='%(asctime)s - %(levelname)s - %(message)s'):
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = f'{log_dir}/load_{timestamp}.log'

    logging.basicConfig(
        filename=log_filename,
        format=format,    # format as time, level, and message
        level=logging.INFO                                      # lowest level you want to capture with logs
    )
    return True


def upload_to_s3(access_key, secret_key, region, bucket, local_file_location="test_upload.json", aws_object_destination="python-import/test_upload.json"):
    """Upload a file to an S3 bucket

    :param bucket: Bucket to upload to
    :param local_file_location: File to upload
    :param aws_object_destination: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
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
        logging.error(e)
        return False
    return True

# Configure logs
configure_logs()
logger = logging.getLogger()
logger.info('Logger initialized')

# Load environment variables from a .env file
load_dotenv()

# Store access credentials
aws_access_key = os.getenv('AWS_ACCESS_KEY')
aws_secret_key = os.getenv('AWS_SECRET_KEY')
region = os.getenv('AWS_REGION')
bucket = os.getenv('AWS_BUCKET_NAME')

# Get amplitude event files
data_dir = Path('../amplitude/data')
local_files = list(data_dir.glob('*.json'))

# Upload files to the S3 bucket
processed = 0

for file in local_files:
    aws_object_destination = f'python-import/{os.path.basename(file)}'
    try:
        result = upload_to_s3(
            access_key=aws_access_key, 
            secret_key=aws_secret_key, 
            region=region, 
            bucket=bucket, 
            local_file_location=file, 
            aws_object_destination=aws_object_destination
        )
        # os.remove(file)
        processed+=1
    except Exception as e:
        logging.error(e)

logging.info(f'{processed} files uploaded to {bucket}')

