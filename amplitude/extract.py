"""
Data extraction using Amplitude's Export API
https://amplitude.com/docs/apis/analytics/export

Requires:
    - Amplitude API and Secret Keys
    - Time parameters formatted as strings (YYYYMMDDTHH)
"""  

# Libraries
import os
import requests
import zipfile     
import gzip        
import shutil     
import tempfile
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load credentials from .env file
load_dotenv()
api_key = os.getenv('AMP_API_KEY')
secret_key = os.getenv('AMP_SECRET_KEY')

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


def make_api_call(params, api_key, secret_key, zip_path='data/response.zip'):
    # API endpoint is the EU residency server
    url = 'https://analytics.eu.amplitude.com/api/2/export'
    params = params

    # Make the GET Request with basic authentication
    response = requests.get(url, params=params, auth=(api_key, secret_key))

    if response.ok:
        # Save the zip file
        logger.info('Data successfully retrieved')
        data = response.content
        with open(zip_path, 'wb') as file:
            file.write(data)
        logger.info('Data has been saved to ./amp_events.zip')
        return True

    else:
        # The request failed. Print the error.
        logger.info(f"Error: {response.status_code} {response.text}")
        return False

def extract_json_files(zip_path):

    # Make a temp dir to open zip files
    temp_dir = tempfile.mkdtemp()

    # Create local output directory
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)
        logger.info(f"Zip file opened in temporary folder located at {temp_dir}")


        # FOR each compressed .gz file inside the zip archive DO
        day_folder = next(f for f in os.listdir(temp_dir) if f.isdigit())
        day_path = Path(os.path.join(temp_dir, day_folder))

        # Walk through the day folder and decompress each .gz file to the data directory
        for root, _, files in os.walk(day_path):
            for file in files:
                if file.endswith('.gz'):
                    gz_path = os.path.join(root, file)
                    json_filename = file[:-3]  # Remove .gz extension
                    output_path = os.path.join(data_dir, json_filename)
                    with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
                        shutil.copyfileobj(gz_file, out_file)
                        logger.info(f'{file} processed')
        
        # Delete the temporary directory
        shutil.rmtree(temp_dir)
        logger.info("All files extracted to the 'data' directory!")

    except Exception as e:
        # Log error
        logger.info(e)


# Format the start and end time strings (YYYYMMDDTHH)
yesterday = datetime.now() - timedelta(days=1)
start_time = yesterday.strftime('%Y%m%dT00')
end_time = yesterday.strftime('%Y%m%dT23')

# Make a data directory
data_dir = 'data'
os.makedirs(data_dir, exist_ok=True)
zip_filename = f'{data_dir}/amp_events.zip'

# Call the function to extract amplitude events
params = {
        'start': start_time,
        'end': end_time
}

amp_events = make_api_call(
    params = params,
    api_key=api_key, 
    secret_key=secret_key, 
    zip_path=zip_filename
)

if amp_events:
    extract_json_files(zip_path=zip_filename)

