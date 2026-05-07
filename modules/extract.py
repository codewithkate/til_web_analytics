# Libraries
import os
import requests
import zipfile     
import gzip        
import shutil     
import tempfile
import json
import time
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

def extract(url, params, api_key, secret_key, data_dir='data', max_tries=3):
    """
    This function makes a GET request with basic authentication. 
    The response is expected to be a .zip file that will be saved to a local data directory.

    Args:
        url (str): _description_
        params (dict): _description_
        api_key (str): _description_
        secret_key (str): _description_
        data_dir (str, optional): _description_. Defaults to 'data'.
        max_tries (int, optional): _description_. Defaults to 3.
    
    Return:
        bool: True if it works, False if it doesn't.
    """
    # Make the GET Request with basic authentication
    count = 0

    while count <= max_tries:
        response = requests.get(url,params, auth=(api_key, secret_key))
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


        if 200 <= response.status_code < 300:
            logger.info('Data successfully retrieved')
            os.makedirs(data_dir, exist_ok=True)
            filename = f'{data_dir}/{timestamp}.zip'
            data = response.content
            with open(filename, 'wb') as file:
                file.write(data)
            logger.info(f'Data has been saved to {filename}')
            return True, filename
            break

        elif response.status_code >= 500:
                # Retry after 10 seconds if server error.
                time.sleep(10)
                count+=1
                logger.info(f'Attempt #{count} to call {url}')

        else:
            # The request failed. Print the error.
            logger.info(f"Error: {response.status_code} {response.text}")
            return False
            break

def decompress_zip(zip_path):
    """
    The function unpackages the first layer of compression (.zip files) from a local data directory.
    Outputs are stored in a temporary directory.

    Args:
        zip_path (Path object): _description_
    """    
    temp_dir = tempfile.mkdtemp()

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)
        logger.info(f"Zip file opened in temporary folder located at {temp_dir}")
        return temp_dir
    except Exception as e:
        logger.info(e)
        return None

def decompress_gzip(temp_dir, data_dir):
    """
    The function unpackages the second layer of compression (.gz files) located in a temporary directory.
    Must run decompress_zip() to create the temporary directory for this function's input and output.

    Args:
        data_dir (_type_): _description_
    """
    # Make a temp dir to open zip files
    try:
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
        return True
        # Delete the temporary directory
        shutil.rmtree(temp_dir)
        logger.info("All files extracted to the 'data' directory!")

    except Exception as e:
        # Log error
        logger.info(e)
        return False     