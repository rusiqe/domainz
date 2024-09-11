from name_com import NameComAPI
from namecheap import NamecheapAPI
import dns.resolver

class DNSManager:
    def __init__(self):
        self.name_com = NameComAPI()
        self.namecheap = NamecheapAPI()

    def get_all_domains(self):
        name_com_domains = self.name_com.get_domains()
        namecheap_domains = self.namecheap.get_domains()
        return name_com_domains + namecheap_domains

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
