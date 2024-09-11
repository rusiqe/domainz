from flask import Flask, render_template, request, redirect, url_for
from database import Database
from dns_manager import DNSManager

app = Flask(__name__)
db = Database('domains.db')
dns_manager = DNSManager(db)

@app.route('/')
def domain_list():
    domains = db.get_domains()
    return render_template('domain_list.html', domains=domains)

@app.route('/domain/<int:domain_id>')
def domain_details(domain_id):
    domain = db.get_domain(domain_id)
    dns_records = db.get_dns_records(domain_id)
    return render_template('domain_details.html', domain=domain, dns_records=dns_records)

@app.route('/domain/<int:domain_id>/update_record', methods=['POST'])
def update_dns_record(domain_id):
    record_id = request.form['record_id']
    record_type = request.form['type']
    host = request.form['host']
    value = request.form['value']
    ttl = int(request.form['ttl'])

    domain = db.get_domain(domain_id)
    dns_manager.update_dns_record(domain['name'], domain['account_id'], record_id, record_type, host, value, ttl)

    return redirect(url_for('domain_details', domain_id=domain_id))

@app.route('/sync_domains')
def sync_domains():
    dns_manager.sync_domains()
    return redirect(url_for('domain_list'))

if __name__ == '__main__':
    app.run(debug=True)
