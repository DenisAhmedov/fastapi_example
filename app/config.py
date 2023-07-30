import os
from pathlib import Path

from dotenv import load_dotenv


dotenv_path = os.path.join(Path(__file__).resolve().parents[1], '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

SECRET_KEY = 'e633e06595569fa8124c2ebb867588869ab70e5c50a191936d96baf9929d0f2e'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 3600
SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db'
EMAIL_HUNTER_API_KEY = os.environ.get('EMAIL_HUNTER_API_KEY') or 'test-api-key'
CLEARBIT_API_KEY = os.environ.get('CLEARBIT_API_KEY') or 'test-api-key'
