import os
os.environ['PYTHONWARNINGS'] = 'ignore:Unverified HTTPS request'

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from dns_manager import DNSManager
from database import get_session, Domain, DNSRecord
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    dns_manager = DNSManager()
    session = get_session()

    try:
        # Fetch all domains
        domains = dns_manager.get_all_domains()

        if not domains:
            logger.warning("No domains retrieved. Check your API credentials and permissions.")
            return

        for domain_name in domains:
            # Check if domain exists in database
            domain = session.query(Domain).filter_by(name=domain_name).first()
            if not domain:
                domain = Domain(name=domain_name, registrar="Unknown")
                session.add(domain)

            # Get DNS records
            dns_records = dns_manager.get_dns_records(domain_name)

            # Update database with DNS records
            for record in dns_records:
                db_record = session.query(DNSRecord).filter_by(
                    domain_id=domain.id,
                    type=record['type'],
                    name=record['name']
                ).first()

                if db_record:
                    db_record.content = record['address']
                    db_record.ttl = record['ttl']
                else:
                    new_record = DNSRecord(
                        domain_id=domain.id,
                        type=record['type'],
                        name=record['name'],
                        content=record['address'],
                        ttl=record['ttl']
                    )
                    session.add(new_record)

            # Check actual DNS
            actual_dns = dns_manager.check_dns(domain_name)
            if actual_dns:
                print(f"Actual DNS for {domain_name}:")
                print(actual_dns)

        session.commit()
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    python3 src/main.py
    main()