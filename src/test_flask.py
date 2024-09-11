from flask import Flask
from database import Database
from dns_manager import DNSManager
from config import config

app = Flask(__name__)
db = Database(config.DATABASE_FILE)
dns_manager = DNSManager(db)

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/domains')
def list_domains():
    domains = db.get_domains()
    return f"Domains: {domains}"

@app.route('/sync')
def sync_domains():
    dns_manager.sync_domains()
    return "Domains synced"

if __name__ == '__main__':
    db.create_tables()
    app.run(debug=True)
