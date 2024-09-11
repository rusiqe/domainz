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
            # ... rest of your domain processing code ...

        session.commit()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()