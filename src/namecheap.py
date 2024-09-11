import requests
import xml.etree.ElementTree as ET
import logging
from config import config

logger = logging.getLogger(__name__)

class NamecheapAPI:
    def __init__(self):
        self.api_user = config.NAMECHEAP_API_USER
        self.api_key = config.NAMECHEAP_API_KEY
        self.client_ip = config.NAMECHEAP_CLIENT_IP
        self.base_url = config.NAMECHEAP_BASE_URL

    def test_connection(self):
        try:
            params = {
                'ApiUser': self.api_user,
                'ApiKey': self.api_key,
                'UserName': self.api_user,
                'ClientIp': self.client_ip,
                'Command': 'namecheap.domains.getList'
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            # Log the raw response content
            logger.debug(f"Namecheap API raw response: {response.content}")
            
            root = ET.fromstring(response.content)
            
            # Check if the response contains an ApiResponse element
            api_response = root.find('ApiResponse')
            if api_response is None:
                logger.error("Namecheap API response doesn't contain an ApiResponse element.")
                return False
            
            # Check the CommandResponse status
            command_response = api_response.find('CommandResponse')
            if command_response is None:
                logger.error("Namecheap API response doesn't contain a CommandResponse element.")
                return False
            
            status = command_response.get('Status')
            if status == "OK":
                logger.info("Namecheap API connection successful")
                return True
            else:
                errors = api_response.findall('.//Errors/Error')
                error_messages = [error.text for error in errors]
                logger.error(f"Namecheap API connection failed. Errors: {', '.join(error_messages)}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Namecheap API connection failed: {e}")
            return False
        except ET.ParseError as e:
            logger.error(f"Failed to parse Namecheap API response: {e}")
            logger.error(f"Response content: {response.content}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error in Namecheap API connection: {e}")
            return False

    def get_domains(self):
        # Implement this method to fetch domains from Namecheap
        # This is a placeholder implementation
        logger.info("Fetching domains from Namecheap")
        return []  # Return an empty list for now

    # ... rest of the class implementation ...
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