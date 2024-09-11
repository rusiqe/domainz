import requests
import yaml

class NameComAPI:
    def __init__(self):
        with open('config/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        self.username = config['name_com']['api_username']
        self.token = config['name_com']['api_token']
        self.base_url = "https://api.name.com/v4"

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
