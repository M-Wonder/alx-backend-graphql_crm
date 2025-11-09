import os
import django
from datetime import datetime
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

def logcrmheartbeat():
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    with open('/tmp/crmheartbeatlog.txt', 'a') as f:
        f.write(f"{timestamp} CRM is alive\n")
    
    # Optional: Query GraphQL hello field
    try:
        url = 'http://localhost:8000/graphql'
        query = '{ hello }'
        response = requests.post(url, json={'query': query}, timeout=5)
        if response.status_code == 200:
            with open('/tmp/crmheartbeatlog.txt', 'a') as f:
                f.write(f"{timestamp} GraphQL endpoint is responsive\n")
    except Exception as e:
        with open('/tmp/crmheartbeatlog.txt', 'a') as f:
            f.write(f"{timestamp} GraphQL endpoint check error: {str(e)}\n")

def updatelowstock():
    try:
        mutation = """
        mutation {
            updateLowStockProducts {
                success
                message
                updatedProducts {
                    id
                    name
                    stock
                }
            }
        }
        """
        url = 'http://localhost:8000/graphql'
        response = requests.post(url, json={'query': mutation})
        data = response.json()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open('/tmp/lowstockupdates_log.txt', 'a') as f:
            if 'errors' in data:
                f.write(f"[{timestamp}] ERROR: {data['errors']}\n")
            else:
                result = data['data']['updateLowStockProducts']
                f.write(f"[{timestamp}] {result['message']}\n")
                if result['success'] and result['updatedProducts']:
                    for product in result['updatedProducts']:
                        f.write(f"[{timestamp}] Updated: {product['name']} - New stock: {product['stock']}\n")
    except Exception as e:
        with open('/tmp/lowstockupdates_log.txt', 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] ERROR: {str(e)}\n")
