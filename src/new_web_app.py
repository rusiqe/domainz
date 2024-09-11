from flask import Flask, render_template, request, redirect, url_for
from database import Database
from dns_manager import DNSManager
from config import config

app = Flask(__name__)
db = Database(config.DATABASE_FILE)
dns_manager = DNSManager(db)

@app.route('/')
def index():
    domains = db.get_domains()
    return render_template('domain_list.html', domains=domains)

if __name__ == '__main__':
    db.create_tables()
    app.run(debug=True)

# ... (previous code remains the same)

@app.route('/domain/<int:domain_id>')
def domain_details(domain_id):
    domain = db.get_domain(domain_id)
    dns_records = db.get_dns_records(domain_id)
    return render_template('domain_details.html', domain=domain, dns_records=dns_records)

# ... (rest of the code)

# ... (previous code remains the same)

@app.route('/sync')
def sync_domains():
    dns_manager.sync_domains()
    return redirect(url_for('index'))

# ... (rest of the code)

# ... (previous code remains the same)

@app.route('/update_record', methods=['POST'])
def update_record():
    domain_id = request.form['domain_id']
    record_id = request.form['record_id']
    record_type = request.form['type']
    host = request.form['host']
    value = request.form['value']
    ttl = request.form['ttl']
    
    dns_manager.update_dns_record(domain_id, record_id, record_type, host, value, ttl)
    return redirect(url_for('domain_details', domain_id=domain_id))

# ... (rest of the code)
