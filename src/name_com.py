import requests
from typing import List, Dict

class NameComAPI:
    def __init__(self, username: str, token: str):
        self.username = username
        self.token = token
        self.base_url = "https://api.name.com/v4"

    def get_domains(self) -> List[Dict]:
        url = f"{self.base_url}/domains"
        headers = {
            "Authorization": f"Basic {self.username}:{self.token}",
            "Content-Type": "application/json",
        }
        params = {
            "page": 1,
            "perPage": 1000
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("domains", [])

    def get_dns_records(self, domain: str) -> List[Dict]:
        url = f"{self.base_url}/domains/{domain}/records"
        headers = {
            "Authorization": f"Basic {self.username}:{self.token}",
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("records", [])

    def update_dns_record(self, domain: str, record_id: str, record_type: str, host: str, answer: str, ttl: int):
        url = f"{self.base_url}/domains/{domain}/records/{record_id}"
        headers = {
            "Authorization": f"Basic {self.username}:{self.token}",
            "Content-Type": "application/json",
        }
        data = {
            "type": record_type,
            "host": host,
            "answer": answer,
            "ttl": ttl
        }

        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

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