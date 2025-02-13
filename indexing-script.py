import requests
import logging
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path to the JSON key file (created dynamically by GitHub Actions)
json_path = 'indexing-index.json'

# Load credentials
try:
    credentials = Credentials.from_service_account_file(
        json_path,
        scopes=['https://www.googleapis.com/auth/indexing']
    )
except FileNotFoundError:
    logger.error(f"Error: {json_path} not found. Ensure the JSON file is created during the workflow run.")
    exit(1)

# Refresh the token
credentials.refresh(Request())

# URL to index
url_to_index = 'https://www.nafirashidrahim.me/'

# Google Indexing API URL
api_url = 'https://indexing.googleapis.com/v3/urlNotifications:publish'

# Body of the request
body = {
    'url': url_to_index,
    'type': 'URL_UPDATED'
}

# Headers with the access token
headers = {
    'Authorization': f'Bearer {credentials.token}',
    'Content-Type': 'application/json'
}

# Send request with a timeout
try:
    response = requests.post(api_url, json=body, headers=headers, timeout=10)  # 10-second timeout
    response.raise_for_status()  # Raise an error for bad status codes
    logger.info(f"Successfully submitted {url_to_index} for indexing.")
    logger.info(f"Full API Response: {response.json()}")  # Log the full API response
except requests.exceptions.RequestException as e:
    logger.error(f"Error: {e}")
    exit(1)