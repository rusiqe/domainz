from database import Database
from name_com import NameComAPI
from namecheap import NamecheapAPI
import dns.resolver
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DNSManager:
    def __init__(self, database: Database):
        self.database = database

    def sync_domains(self):
        accounts = self.database.get_accounts()
        for account in accounts:
            if account['registrar'] == 'name.com':
                api = NameComAPI(account['username'], account['api_key'])
            elif account['registrar'] == 'namecheap':
                api = NamecheapAPI(account['username'], account['api_key'], account['username'], account['api_secret'])
            else:
                continue

            domains = api.get_domains()
            for domain in domains:
                self.database.add_domain(domain['name'], account['id'])

    def get_dns_records(self, domain_name: str, account_id: int):
        account = self.database.get_account(account_id)
        if account['registrar'] == 'name.com':
            api = NameComAPI(account['username'], account['api_key'])
        elif account['registrar'] == 'namecheap':
            api = NamecheapAPI(account['username'], account['api_key'], account['username'], account['api_secret'])
        else:
            return []

        return api.get_dns_records(domain_name)

    def update_dns_record(self, domain_name: str, account_id: int, record_id: str, record_type: str, host: str, value: str, ttl: int):
        account = self.database.get_account(account_id)
        if account['registrar'] == 'name.com':
            api = NameComAPI(account['username'], account['api_key'])
            api.update_dns_record(domain_name, record_id, record_type, host, value, ttl)
        elif account['registrar'] == 'namecheap':
            api = NamecheapAPI(account['username'], account['api_key'], account['username'], account['api_secret'])
            api.update_dns_record(domain_name, record_type, host, value, ttl, record_id)

        self.database.update_dns_record(record_id, record_type, host, value, ttl)

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
