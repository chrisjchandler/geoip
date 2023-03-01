from flask import Flask, request, jsonify
import geoip2.database
import os

app = Flask(__name__)

# Path to the MaxMind GeoIP2 database file
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'GeoLite2-ASN.mmdb')

# Function to retrieve the geo-location information for an IP address
def get_geoip_info(ip_address):
    with geoip2.database.Reader(DATABASE_PATH) as reader:
        try:
            response = reader.asn(ip_address)
            return {
                'ip_address': ip_address,
                'asn': response.autonomous_system_number,
                'isp': response.autonomous_system_organization
            }
        except geoip2.errors.AddressNotFoundError:
            return None

# Route to handle the IP address lookup
@app.route('/geoip', methods=['GET'])
def geoip():
    ip_address = request.args.get('ip_address')
    if ip_address:
        geoip_info = get_geoip_info(ip_address)
        if geoip_info:
            return jsonify(geoip_info)
        else:
            return jsonify({'error': 'IP address not found'}), 404
    else:
        return jsonify({'error': 'IP address required'}), 400

if __name__ == '__main__':
    app.run(port=8083)
