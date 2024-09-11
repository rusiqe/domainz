import logging
from typing import List
import requests
import xml.etree.ElementTree as ET
from config import config

logger = logging.getLogger(__name__)

def get_domains_namecheap(api_user: str, api_key: str, username: str, client_ip: str) -> List[str]:
    base_url = "https://api.namecheap.com/xml.response"
    params = {
        "ApiUser": api_user,
        "ApiKey": api_key,
        "UserName": username,
        "Command": "namecheap.domains.getList",
        "ClientIp": client_ip,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        # Log the raw response for debugging
        logger.debug(f"Namecheap API raw response: {response.text}")

        root = ET.fromstring(response.content)
        
        # Check if the API response contains an error
        error_element = root.find(".//Errors/Error")
        if error_element is not None:
            logger.error(f"Namecheap API returned an error: {error_element.text}")
            return []

        domains = root.findall(".//Domain")
        domain_names = [domain.get("Name") for domain in domains]
        
        logger.info(f"Retrieved {len(domain_names)} domains from Namecheap")
        return domain_names
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve domains from Namecheap: {str(e)}")
    except ET.ParseError as e:
        logger.error(f"Failed to parse Namecheap API response: {str(e)}")
    
    return []

import requests
import xml.etree.ElementTree as ET
from typing import List, Dict

class NamecheapAPI:
    def __init__(self, api_user: str, api_key: str, username: str, client_ip: str):
        self.api_user = api_user
        self.api_key = api_key
        self.username = username
        self.client_ip = client_ip
        self.base_url = "https://api.namecheap.com/xml.response"

    def _api_request(self, command: str, params: Dict = None) -> ET.Element:
        default_params = {
            "ApiUser": self.api_user,
            "ApiKey": self.api_key,
            "UserName": self.username,
            "ClientIp": self.client_ip,
            "Command": command,
        }
        if params:
            default_params.update(params)

        response = requests.get(self.base_url, params=default_params)
        response.raise_for_status()
        return ET.fromstring(response.content)

    def get_domains(self) -> List[Dict]:
        root = self._api_request("namecheap.domains.getList")
        domains = root.findall(".//Domain")
        return [domain.attrib for domain in domains]

    def get_dns_records(self, domain: str) -> List[Dict]:
        params = {"SLD": domain.split('.')[0], "TLD": domain.split('.')[1]}
        root = self._api_request("namecheap.domains.dns.getHosts", params)
        records = root.findall(".//host")
        return [record.attrib for record in records]

    def update_dns_record(self, domain: str, record_type: str, host: str, address: str, ttl: int, record_id: str = None):
        sld, tld = domain.split('.')
        params = {
            "SLD": sld,
            "TLD": tld,
            "HostName1": host,
            "RecordType1": record_type,
            "Address1": address,
            "TTL1": ttl,
        }
        if record_id:
            params["HostId1"] = record_id

        root = self._api_request("namecheap.domains.dns.setHosts", params)
        return root.find(".//DomainDNSSetHostsResult").attrib["IsSuccess"] == "true"
        return root.find(".//DomainDNSSetHostsResult").get('IsSuccess') == 'true'