import requests
import xml.etree.ElementTree as ET
import yaml

class NamecheapAPI:
    def __init__(self):
        with open('config/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        self.api_user = config['namecheap']['api_user']
        self.api_key = config['namecheap']['api_key']
        self.client_ip = config['namecheap']['client_ip']
        self.base_url = "https://api.namecheap.com/xml.response"

    def _make_request(self, command, params=None):
        if params is None:
            params = {}
        
        params.update({
            'ApiUser': self.api_user,
            'ApiKey': self.api_key,
            'UserName': self.api_user,
            'ClientIp': self.client_ip,
            'Command': command
        })

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return ET.fromstring(response.content)

    def get_domains(self):
        root = self._make_request('namecheap.domains.getList')
        domains = []
        for domain in root.findall(".//Domain"):
            domains.append(domain.get('Name'))
        return domains

    def get_dns_records(self, domain):
        sld, tld = domain.split('.', 1)
        root = self._make_request('namecheap.domains.dns.getHosts', {
            'SLD': sld,
            'TLD': tld
        })
        records = []
        for record in root.findall(".//host"):
            records.append({
                'id': record.get('HostId'),
                'type': record.get('Type'),
                'name': record.get('Name'),
                'address': record.get('Address'),
                'ttl': record.get('TTL')
            })
        return records

    def create_dns_record(self, domain, record_type, host, address, ttl):
        sld, tld = domain.split('.', 1)
        params = {
            'SLD': sld,
            'TLD': tld,
            'HostName1': host,
            'RecordType1': record_type,
            'Address1': address,
            'TTL1': ttl
        }
        root = self._make_request('namecheap.domains.dns.setHosts', params)
        return root.find(".//DomainDNSSetHostsResult").get('IsSuccess') == 'true'

    def delete_dns_record(self, domain, record_id):
        # Namecheap doesn't have a direct method to delete a single record
        # We need to get all records, remove the one we want to delete, and set the remaining records
        sld, tld = domain.split('.', 1)
        current_records = self.get_dns_records(domain)
        new_records = [r for r in current_records if r['id'] != record_id]

        params = {
            'SLD': sld,
            'TLD': tld
        }

        for i, record in enumerate(new_records, 1):
            params[f'HostName{i}'] = record['name']
            params[f'RecordType{i}'] = record['type']
            params[f'Address{i}'] = record['address']
            params[f'TTL{i}'] = record['ttl']

        root = self._make_request('namecheap.domains.dns.setHosts', params)
        return root.find(".//DomainDNSSetHostsResult").get('IsSuccess') == 'true'
