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
            return True
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

