from dns_manager import DNSManager
from database import get_session, Domain, DNSRecord

def main():
    dns_manager = DNSManager()
    session = get_session()

    # Fetch all domains
    domains = dns_manager.get_all_domains()

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

if __name__ == "__main__":
    main()
