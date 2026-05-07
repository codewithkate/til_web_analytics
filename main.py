# Libraries
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from modules.log import setup_logging
from modules.extract import extract

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

# Extract amplitude events
# Format Amplitude API's time parameters (YYYYMMDDTHH)
yesterday = datetime.now() - timedelta(days=1)
start_time = yesterday.strftime('%Y%m%dT00')
end_time = yesterday.strftime('%Y%m%dT23')

params = {'start': start_time, 'end': end_time}

result = extract(AMP_URL, params, AMP_API_KEY, AMP_SECRET_KEY, 'data')
print(result)