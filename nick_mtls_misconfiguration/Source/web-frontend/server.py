from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Configure URLs from environment variables with defaults
PROD_PKI_URL = os.getenv('PROD_PKI_URL', 'http://localhost:8001')
DEV_PKI_URL = os.getenv('DEV_PKI_URL', 'http://localhost:8000')
NGINX_URL = os.getenv('NGINX_URL', 'https://localhost')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/config')
def get_config():
    return {
        'prod_pki_url': PROD_PKI_URL,
        'dev_pki_url': DEV_PKI_URL,
        'nginx_url': NGINX_URL
    }

@app.route('/api/test-prod-pki')
def test_prod_pki():
    try:
        response = requests.get(f"{PROD_PKI_URL}/issue?username=user", timeout=5)
        if response.status_code == 200:
            return "✅ Prod PKI is working! Response received.\n\n" + response.text[:200] + "..."
        else:
            return f"❌ Prod PKI returned status {response.status_code}"
    except Exception as e:
        return f"❌ Error connecting to Prod PKI: {str(e)}"

# Hidden endpoint for dev PKI (not advertised in UI)
@app.route('/api/test-dev-pki')
def test_dev_pki():
    try:
        response = requests.get(f"{DEV_PKI_URL}/issue?username=test", timeout=5)
        if response.status_code == 200:
            return "✅ Dev PKI is working! Response received.\n\n" + response.text[:200] + "..."
        else:
            return f"❌ Dev PKI returned status {response.status_code}"
    except Exception as e:
        return f"❌ Error connecting to Dev PKI: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 