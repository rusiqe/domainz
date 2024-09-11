import logging
import requests
from typing import List
from config import Config

logger = logging.getLogger(__name__)

class NameComAPI:
    def __init__(self):
        config = Config()
        self.username = config.NAME_COM_API_USERNAME
        self.token = config.NAME_COM_API_TOKEN
        self.base_url = "https://api.name.com/v4"

    def get_domains(self) -> List[str]:
        url = f"{self.base_url}/domains"
        headers = {
            "Authorization": f"Basic {self.username}:{self.token}",
            "Content-Type": "application/json",
        }
        params = {
            "page": 1,
            "perPage": 1000
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            domains = data.get("domains", [])
            domain_names = [domain["domainName"] for domain in domains]
            logger.info(f"Retrieved {len(domain_names)} domains from Name.com")
            return domain_names
        except requests.RequestException as e:
            logger.error(f"Failed to retrieve domains from Name.com: {str(e)}")
            return []

    def test_connection(self) -> bool:
        url = f"{self.base_url}/hello"
        headers = {
            "Authorization": f"Basic {self.username}:{self.token}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                logger.info("Name.com API connection successful")
                return True
            else:
                logger.error(f"Name.com API connection failed. Status code: {response.status_code}")
                return False
        except requests.RequestException as e:
            logger.error(f"Name.com API connection failed: {str(e)}")
            return False
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