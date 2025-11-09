#!/usr/bin/env python3

import requests
import json
from datetime import datetime, timedelta

def send_order_reminders():
    # GraphQL endpoint
    url = 'http://localhost:8000/graphql'
    
    # Calculate date 7 days ago
    one_week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    # GraphQL query for pending orders from the last week
    query = """
    query {
        pendingOrders(startDate: "%s") {
            id
            orderDate
            customer {
                email
            }
        }
    }
    """ % one_week_ago
    
    try:
        # Send GraphQL request using requests (not gql)
        response = requests.post(url, json={'query': query})
        data = response.json()
        
        if 'errors' in data:
            raise Exception(f"GraphQL errors: {data['errors']}")
        
        orders = data['data']['pendingOrders']
        
        # Log order reminders
        with open('/tmp/order_reminders_log.txt', 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] Processing {len(orders)} order reminders\n")
            
            for order in orders:
                f.write(f"[{timestamp}] Order ID: {order['id']}, Customer Email: {order['customer']['email']}\n")
        
        print("Order reminders processed!")
        
    except Exception as e:
        # Log any errors
        with open('/tmp/order_reminders_log.txt', 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] ERROR: {str(e)}\n")
        print(f"Error: {e}")

if __name__ == "__main__":
    send_order_reminders()
