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
import json
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
        with open('./data/data.zip', 'wb') as file:
          file.write(data)
        print('The data.zip file has been saved 💌')
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
amp_call = extract_amplitude_data(start_time=start_time, end_time=end_time, api_key=api_key, secret_key=secret_key)
