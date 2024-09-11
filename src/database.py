import sqlite3
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_file: str):
        self.db_file = db_file

    def _execute_query(self, query: str, params: tuple = ()):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def create_tables(self):
        self._execute_query('''
            CREATE TABLE IF NOT EXISTS domains (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                registrar TEXT NOT NULL,
                account_username TEXT NOT NULL
            )
        ''')
        self._execute_query('''
            CREATE TABLE IF NOT EXISTS dns_records (
                id INTEGER PRIMARY KEY,
                domain_id INTEGER,
                type TEXT NOT NULL,
                host TEXT NOT NULL,
                value TEXT NOT NULL,
                ttl INTEGER,
                FOREIGN KEY (domain_id) REFERENCES domains (id)
            )
        ''')
        # Add a new table for accounts
        self._execute_query('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY,
                registrar TEXT NOT NULL,
                username TEXT NOT NULL,
                api_key TEXT NOT NULL,
                api_secret TEXT
            )
        ''')

    def add_domain(self, name: str, registrar: str, account_username: str):
        self._execute_query(
            "INSERT OR REPLACE INTO domains (name, registrar, account_username) VALUES (?, ?, ?)",
            (name, registrar, account_username)
        )
    def get_domains(self) -> List[Dict]:
        cursor = self._execute_query("SELECT * FROM domains")
        domains = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        logger.info(f"Retrieved {len(domains)} domains from the database")
        return domains
    def get_domain(self, domain_id: int) -> Dict:
        cursor = self._execute_query("SELECT * FROM domains WHERE id = ?", (domain_id,))
        return dict(zip([column[0] for column in cursor.description], cursor.fetchone()))

    def add_dns_record(self, domain_id: int, record_type: str, host: str, value: str, ttl: int):
        self._execute_query(
            "INSERT INTO dns_records (domain_id, type, host, value, ttl) VALUES (?, ?, ?, ?, ?)",
            (domain_id, record_type, host, value, ttl)
        )

    def get_dns_records(self, domain_id: int) -> List[Dict]:
        cursor = self._execute_query("SELECT * FROM dns_records WHERE domain_id = ?", (domain_id,))
        return [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

    def update_dns_record(self, record_id: int, record_type: str, host: str, value: str, ttl: int):
        self._execute_query(
            "UPDATE dns_records SET type = ?, host = ?, value = ?, ttl = ? WHERE id = ?",
            (record_type, host, value, ttl, record_id)
        )

    def add_account(self, registrar: str, username: str, api_key: str, api_secret: str = None):
        self._execute_query(
            "INSERT INTO accounts (registrar, username, api_key, api_secret) VALUES (?, ?, ?, ?)",
            (registrar, username, api_key, api_secret)
        )

    def get_accounts(self) -> List[Dict]:
        cursor = self._execute_query("SELECT * FROM accounts")
        return [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]