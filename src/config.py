import os
from dotenv import load_dotenv
import yaml

# Load environment variables from .env file
load_dotenv()

# Load non-sensitive configuration from YAML
with open('config/config.yaml', 'r') as f:
    yaml_config = yaml.safe_load(f)

class Config:
    # Name.com configuration
    NAME_COM_API_USERNAME = os.getenv('NAME_COM_API_USERNAME')
    NAME_COM_API_TOKEN = os.getenv('NAME_COM_API_TOKEN')
    NAME_COM_BASE_URL = yaml_config['name_com']['base_url']

    # Namecheap configuration
    NAMECHEAP_API_USER = os.getenv('NAMECHEAP_API_USER')
    NAMECHEAP_API_KEY = os.getenv('NAMECHEAP_API_KEY')
    NAMECHEAP_CLIENT_IP = os.getenv('NAMECHEAP_CLIENT_IP')
    NAMECHEAP_BASE_URL = yaml_config['namecheap']['base_url']

    # Database configuration
    DATABASE_URL = os.getenv('DATABASE_URL') if yaml_config['database']['use_env_url'] else yaml_config['database']['url']

config = Config()