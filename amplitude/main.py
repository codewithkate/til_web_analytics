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
import requests
import json
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load .env file
load_dotenv()

# authorization: https://pypi.org/project/python-dotenv/
api_key = os.getenv('AMP_API_KEY')
secret_key = os.getenv('AMP_SECRET_KEY')


# Refresh Schedule: https://docs.python.org/3/library/datetime.html
end_time = datetime.now()
start_time = end_time - timedelta(days=7)

# API endpoint is the EU residency server
url = 'https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': start_time,
    'end': end_time
}

# Make the GET request with basic authentication
response = requests.get(url, params=params, auth=(api_key, secret_key))
