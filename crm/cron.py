import os
import django
from datetime import datetime
import requests
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

def log_crm_heartbeat():
    """Log CRM heartbeat every 5 minutes"""
    try:
        timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
            f.write(f"{timestamp} CRM is alive\n")
    except Exception as e:
        print(f"Heartbeat logging failed: {e}")

def update_low_stock():
    """Update low stock products every 12 hours"""
    try:
        from datetime import datetime
        
        # GraphQL mutation
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
