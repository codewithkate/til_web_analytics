"""
Data extraction using Amplitude's Export API
https://amplitude.com/docs/apis/analytics/export

Requires:
    - Amplitude API and Secret Keys
    - Time parameters of the form:
        - start_time = '20241101T00'  
        - end_time = '20241101T23'
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
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load .env file
load_dotenv()

def extract_amplitude_data(start_time, end_time, api_key, secret_key):
    # API endpoint is the EU residency server
    url = 'https://analytics.eu.amplitude.com/api/2/export'
    params = {
        'start': start_time,
        'end': end_time
    }

    # Make the GET Request with basic authentication
    response = requests.get(url, params=params, auth=(api_key, secret_key))

    if response.status_code == 200:
        # The request was successful. Extract the data.
        print('Data successfully retrieved 🥳')
        data = response.content
        # Save the zip file
        with open('amp_events.zip', 'wb') as file:
            file.write(data)
        print('Data has been saved to ./amp_events.zip 💌')
        return True

    else:
        # The request failed. Print the error.
        print(f"Error: {response.status_code} {response.text}")
        return False
    

# Read .env file
api_key = os.getenv('AMP_API_KEY')
secret_key = os.getenv('AMP_SECRET_KEY')

# Format the start and end time strings (YYYYMMDDTHH)
yesterday = datetime.now() - timedelta(days=1)
start_time = yesterday.strftime('%Y%m%dT00')
end_time = yesterday.strftime('%Y%m%dT23')

# Call the function to extract amplitude events
amp_events = extract_amplitude_data(start_time=start_time, end_time=end_time, api_key=api_key, secret_key=secret_key)

def extract_json_files(zip_path):

    # Make a temp dir to open zip files
    temp_dir = tempfile.mkdtemp()
    # Create local output directory
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)
        # LOG size of the zip file
        # LOG "Zip file opened successfully"
        print("Zip file opened successfully")


        day_folder = next(f for f in os.listdir(temp_dir) if f.isdigit())
        day_path = os.path.join(temp_dir, day_folder)
        

        # FOR each compressed .gz file inside the zip archive DO
        for root, _, files in os.walk(day_path):
            for file in files:
                if file.endswith('.gz'):
                    # OPEN the .gz file and decompress it
                    gz_path = os.path.join(root, file)
                    json_filename = file[:-3] # remove gz extension  
                    output_path = os.path.join(data_dir, json_filename)

                    # COPY gz file to output file
                    with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'w') as out_file:
                        data = [json.loads(line) for line in gz_file]
                        json.dump(data, out_file)
                    # LOG ".gz file decompressed successfully"
                    print(f"{json_filename} decompressed successfully")
        
    except Exception as e:
        # Log error
        print(e)

if amp_events:
    extract_json_files(zip_path="amp_events.zip")

