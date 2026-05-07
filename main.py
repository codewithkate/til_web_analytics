# Libraries
import os
import shutil
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timedelta
from modules.log import setup_logging
from modules.extract import extract, decompress_zip, decompress_gzip
from modules.load import upload_to_s3

logger = setup_logging()
logger.info('Logger initialized.')

# Load credentials from .env file
load_dotenv()
AMP_API_KEY = os.getenv('AMP_API_KEY')
AMP_SECRET_KEY = os.getenv('AMP_SECRET_KEY')
AMP_DATA_REGION = os.getenv('AMP_DATA_REGION')
if AMP_DATA_REGION=='EU':
    AMP_URL = os.getenv('AMP_EU_URL')
else:
    AMP_URL = os.getenv('AMP_URL')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
region = os.getenv('AWS_REGION')
bucket = os.getenv('AWS_BUCKET_NAME')
bucket_object = os.getenv('AWS_BUCKET_OBJECT')

# Extract amplitude events
# Format Amplitude API's time parameters (YYYYMMDDTHH)
yesterday = datetime.now() - timedelta(days=1)
start_time = yesterday.strftime('%Y%m%dT00')
end_time = yesterday.strftime('%Y%m%dT23')

params = {'start': start_time, 'end': end_time}
data_dir = Path('data')

result, zip_path = extract(AMP_URL, params, AMP_API_KEY, AMP_SECRET_KEY, data_dir)
print(result)
print(zip_path)

if result:
    temp_dir = decompress_zip(zip_path)
    print(temp_dir)
    process = decompress_gzip(temp_dir, data_dir)
    local_files = list(data_dir.glob('*.json'))
    print(local_files)
    
    processed = 0
    
    try: 
        for file in local_files:
            local_file_location = file
            aws_object_destination = f'{bucket_object}/{os.path.basename(file)}'
            upload_to_s3(AWS_ACCESS_KEY, AWS_SECRET_KEY, region, bucket, local_file_location, aws_object_destination)
            os.remove(file)
            processed+=1
    except Exception as e:
        logger.error(e)

logger.info(f'{processed} files uploaded to {bucket}/{bucket_object}')
shutil.rmtree(data_dir)