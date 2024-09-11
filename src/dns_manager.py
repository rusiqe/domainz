from name_com import NameComAPI
from namecheap import NamecheapAPI
import dns.resolver
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DNSManager:
    def __init__(self):
        self.name_com = NameComAPI()
        self.namecheap = NamecheapAPI()

    def get_all_domains(self):
        domains = []
        try:
            name_com_domains = self.name_com.get_domains()
            domains.extend(name_com_domains)
            logger.info(f"Retrieved {len(name_com_domains)} domains from Name.com")
        except Exception as e:
            logger.error(f"Error retrieving domains from Name.com: {str(e)}")

        try:
            namecheap_domains = self.namecheap.get_domains()
            domains.extend(namecheap_domains)
            logger.info(f"Retrieved {len(namecheap_domains)} domains from Namecheap")
        except Exception as e:
            logger.error(f"Error retrieving domains from Namecheap: {str(e)}")

        return domains
    def get_dns_records(self, domain):
        try:
            return self.name_com.get_dns_records(domain)
        except:
            return self.namecheap.get_dns_records(domain)

    def create_dns_record(self, domain, record_type, host, answer, ttl):
        try:
            return self.name_com.create_dns_record(domain, record_type, host, answer, ttl)
        except:
            return self.namecheap.create_dns_record(domain, record_type, host, answer, ttl)

    def delete_dns_record(self, domain, record_id):
        try:
            return self.name_com.delete_dns_record(domain, record_id)
        except:
            return self.namecheap.delete_dns_record(domain, record_id)

    def check_dns(self, domain):
        try:
            a_records = dns.resolver.resolve(domain, 'A')
            mx_records = dns.resolver.resolve(domain, 'MX')
            txt_records = dns.resolver.resolve(domain, 'TXT')
            
            return {
                'A': [str(r) for r in a_records],
                'MX': [str(r) for r in mx_records],
                'TXT': [str(r) for r in txt_records]
            }
        except dns.resolver.NXDOMAIN:
            return None
