import os
from flask import Flask, render_template, request, redirect, url_for
from database import Database
from dns_manager import DNSManager
from config import config

# Get the absolute path of the directory containing this file
base_dir = os.path.abspath(os.path.dirname(__file__))
# Go up one level to the project root
project_root = os.path.dirname(base_dir)
# Set the template folder path
template_dir = os.path.join(project_root, 'templates')

app = Flask(__name__, template_folder=template_dir)
db = Database(config.DATABASE_FILE)
dns_manager = DNSManager(db)  # This line is now correct

@app.route('/')
def index():
    domains = db.get_domains()
    print("Retrieved domains:", domains)  # Debug print
    return render_template('domain_list.html', domains=domains)

# ... (rest of your routes)

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
