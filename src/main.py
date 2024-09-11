import warnings
import urllib3
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)

from dns_manager import DNSManager
from database import get_session, Domain, DNSRecord
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    dns_manager = DNSManager()
    session = get_session()

    # Test API connections
    name_com_connected = dns_manager.name_com.test_connection()
    namecheap_connected = dns_manager.namecheap.test_connection()

    if not (name_com_connected or namecheap_connected):
        logger.error("Failed to connect to both Name.com and Namecheap APIs. Please check your credentials and network connection.")
        return

    try:
        # Fetch all domains
        domains = []
        if name_com_connected:
            name_com_domains = dns_manager.name_com.get_domains()
            domains.extend(name_com_domains)

        if namecheap_connected:
            namecheap_domains = dns_manager.namecheap.get_domains()
            domains.extend(namecheap_domains)

        if not domains:
            logger.warning("No domains retrieved. Check your API credentials and permissions.")
            return

        for domain_name in domains:
            logger.info(f"Processing domain: {domain_name}")
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
                logger.info(f"Actual DNS for {domain_name}:")
                logger.info(actual_dns)

        session.commit()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()