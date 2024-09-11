import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_FILE = os.getenv('DATABASE_FILE', 'domains.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')

    NAME_COM_ACCOUNTS = [
        {
            'username': os.getenv(f'NAME_COM_USERNAME_{i}'),
            'token': os.getenv(f'NAME_COM_TOKEN_{i}')
        }
        for i in range(1, 6)  # Assuming up to 5 Name.com accounts
    ]

    NAMECHEAP_ACCOUNTS = [
        {
            'api_user': os.getenv(f'NAMECHEAP_API_USER_{i}'),
            'api_key': os.getenv(f'NAMECHEAP_API_KEY_{i}'),
            'username': os.getenv(f'NAMECHEAP_USERNAME_{i}'),
            'client_ip': os.getenv(f'NAMECHEAP_CLIENT_IP_{i}')
        }
        for i in range(1, 6)  # Assuming up to 5 Namecheap accounts
    ]

config = Config()
