import requests
import logging
from config import config

logger = logging.getLogger(__name__)

class NameComAPI:
    def __init__(self):
        self.username = config.NAME_COM_API_USERNAME
        self.token = config.NAME_COM_API_TOKEN
        self.base_url = config.NAME_COM_BASE_URL

    def test_connection(self):
        url = f"{self.base_url}/hello"
        try:
            response = requests.get(url, auth=(self.username, self.token))
            response.raise_for_status()
            logger.info("Name.com API connection successful")
            return True
        except requests.exceptions.HTTPError as e:
            logger.error(f"Name.com API connection failed: {e}")
            logger.error(f"Response content: {e.response.content}")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Name.com API connection failed: {e}")
            return False

    def get_domains(self):
        url = f"{self.base_url}/domains"
        try:
            response = requests.get(url, auth=(self.username, self.token))
            response.raise_for_status()
            domains = response.json().get('domains', [])
            logger.info(f"Retrieved {len(domains)} domains from Name.com")
            return [domain['domainName'] for domain in domains]
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching domains from Name.com: {e}")
            return []

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
