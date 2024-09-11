import logging
from database import Database
from name_com import NameComAPI
from namecheap import NamecheapAPI
from config import config

# import dns.resolver

logger = logging.getLogger(__name__)

class DNSManager:
    def __init__(self, database: Database):
        self.database = database

    def sync_domains(self):
        total_domains = 0

        # Sync domains from Name.com accounts
        for account in config.NAME_COM_ACCOUNTS:
            if account['username'] and account['token']:
                api = NameComAPI(account['username'], account['token'])
                domains = api.get_domains()
                logger.info(f"Retrieved {len(domains)} domains from Name.com account {account['username']}")
                for domain in domains:
                    self.database.add_domain(domain['domainName'], 'name.com', account['username'])
                total_domains += len(domains)

        # Sync domains from Namecheap accounts
        for account in config.NAMECHEAP_ACCOUNTS:
            if all(account.values()):  # Check if all required fields are present
                api = NamecheapAPI(account['api_user'], account['api_key'], account['username'], account['client_ip'])
                domains = api.get_domains()
                logger.info(f"Retrieved {len(domains)} domains from Namecheap account {account['username']}")
                for domain in domains:
                    self.database.add_domain(domain['Name'], 'namecheap', account['username'])
                total_domains += len(domains)

        logger.info(f"Total domains synced: {total_domains}")

    def update_dns_record(self, domain_id: int, record_id: str, record_type: str, host: str, value: str, ttl: int):
        domain = self.database.get_domain(domain_id)
        if domain['registrar'] == 'name.com':
            account = next((acc for acc in config.NAME_COM_ACCOUNTS if acc['username'] == domain['account_username']), None)
            if account:
                api = NameComAPI(account['username'], account['token'])
                api.update_dns_record(domain['name'], record_id, record_type, host, value, ttl)
        elif domain['registrar'] == 'namecheap':
            account = next((acc for acc in config.NAMECHEAP_ACCOUNTS if acc['username'] == domain['account_username']), None)
            if account:
                api = NamecheapAPI(account['api_user'], account['api_key'], account['username'], account['client_ip'])
                api.update_dns_record(domain['name'], record_type, host, value, ttl, record_id)

        self.database.update_dns_record(record_id, record_type, host, value, ttl)            return None