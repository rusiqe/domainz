import requests
import logging
from config import config

logger = logging.getLogger(__name__)

class NameComAPI:
    def __init__(self):
        self.username = config.NAME_COM_API_USERNAME
        self.token = config.NAME_COM_API_TOKEN
        self.base_url = config.NAME_COM_BASE_URL
    def get_domains(self):
        url = f"{self.base_url}/domains"
        response = requests.get(url, auth=(self.username, self.token))
        response.raise_for_status()
        return response.json()['domains']

    def get_dns_records(self, domain):
        url = f"{self.base_url}/domains/{domain}/records"
        response = requests.get(url, auth=(self.username, self.token))
        response.raise_for_status()
        return response.json()['records']

    def create_dns_record(self, domain, record_type, host, answer, ttl):
        url = f"{self.base_url}/domains/{domain}/records"
        data = {
            "type": record_type,
            "host": host,
            "answer": answer,
            "ttl": ttl
        }
        response = requests.post(url, json=data, auth=(self.username, self.token))
        response.raise_for_status()
        return response.json()

    def delete_dns_record(self, domain, record_id):
        url = f"{self.base_url}/domains/{domain}/records/{record_id}"
        response = requests.delete(url, auth=(self.username, self.token))
        response.raise_for_status()
        return response.json()
