import logging
from database import Database
from dns_manager import DNSManager
from new_web_app import app
from config import config

# Configure logging for all modules
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    db = Database(config.DATABASE_FILE)
    db.create_tables()

    dns_manager = DNSManager(db)
    dns_manager.sync_domains()

    domains = db.get_domains()
    if domains:
        logger.info(f"Successfully synced {len(domains)} domains")
    else:
        logger.warning("No domains were synced. Check your API credentials and internet connection.")

    logger.info("Starting the web application...")
    app.run(debug=True)    app.run(debug=True)
