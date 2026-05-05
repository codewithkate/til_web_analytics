"""
Data Loading into a S3 bucket using boto3

Requirements:
    - personlized aws templates
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
from datetime import datetime
from pathlib import Path


# Configure logs
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_filename = f'{log_dir}/load_{timestamp}.log'

logging.basicConfig(
    filename=log_filename,
    format='%(asctime)s - %(levelname)s - %(message)s',    # format as time, level, and message
    level=logging.INFO                                      # lowest level you want to capture with logs
)

logger = logging.getLogger()
logger.info('Logger initialized')

# Load environment variables from a .env file
load_dotenv()

# Store access credentials
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket = os.getenv('AWS_BUCKET_NAME')

# Create a boto3 client/resource
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Upload amplitude events to the S3 bucket
data_dir = Path('amplitude/data')
files = list(data_dir.glob('*.json'))

processed = 0

for file in files:
    filename = os.path.basename(file)
    try:
        s3_client.upload_file(file, bucket, filename)
        logger.info(f'{file} uploaded to S3')
        s3_client.head_object(Bucket=bucket, Key=filename) # only return metadata
        os.remove(file)
        logger.info(f'{file} deleted')
        processed+=1
    except Exception as e:
        logging.error(e)

logging.info(f'{processed} files uploaded')