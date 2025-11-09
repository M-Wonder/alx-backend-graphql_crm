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
        # Log basic heartbeat
        timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')

        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
            f.write(f"{timestamp} CRM is alive\n")

        # Optional: Verify GraphQL endpoint is responsive
        try:
            url = 'http://localhost:8000/graphql'
            query = '{ hello }'

            response = requests.post(url, json={'query': query}, timeout=5)

            if response.status_code == 200:
                with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
                    f.write(f"{timestamp} GraphQL endpoint is responsive\n")
            else:
                with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
                    f.write(f"{timestamp} GraphQL endpoint check failed: Status {response.status_code}\n")

        except Exception as e:
            with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
                f.write(f"{timestamp} GraphQL endpoint check error: {str(e)}\n")

    except Exception as e:
        # Fallback logging if file writing fails
        print(f"Heartbeat logging failed: {e}")

def update_low_stock():
    """Update low stock products every 12 hours"""
    try:
        import requests
        import json
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
