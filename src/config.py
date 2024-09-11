import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_FILE = os.getenv('DATABASE_FILE', 'domains.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    NAMECHEAP_CLIENT_IP = os.getenv('NAMECHEAP_CLIENT_IP')

Flask==2.0.1
requests==2.26.0
python-dotenv==0.19.0
