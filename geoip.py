from flask import Flask, jsonify, render_template, request
from geoip2 import database

app = Flask(__name__)

# Replace the path with the actual path to the GeoLite2-ASN.mmdb file
DATABASE_PATH = 'GeoLite2-ASN.mmdb'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/geoip', methods=['GET'])
def geoip():
    ip_address = request.args.get('ip')
    if ip_address:
        with database.Reader(DATABASE_PATH) as reader:
            response = reader.asn(ip_address)
            return jsonify({'asn': response.autonomous_system_number, 'org': response.autonomous_system_organization})
    else:
        return 'Please provide an IP address.'

if __name__ == '__main__':
    app.run()

