import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    NAME_COM_API_USERNAME = os.getenv('NAME_COM_API_USERNAME')
    NAME_COM_API_TOKEN = os.getenv('NAME_COM_API_TOKEN')
    NAMECHEAP_API_USER = os.getenv('NAMECHEAP_API_USER')
    NAMECHEAP_API_KEY = os.getenv('NAMECHEAP_API_KEY')
    NAMECHEAP_USERNAME = os.getenv('NAMECHEAP_USERNAME')
    NAMECHEAP_CLIENT_IP = os.getenv('NAMECHEAP_CLIENT_IP')