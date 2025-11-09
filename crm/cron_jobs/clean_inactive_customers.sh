#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Execute Python command to delete inactive customers
python manage.py shell << PYTHON_EOF
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer, Order
import datetime

# Calculate date one year ago
one_year_ago = timezone.now() - timedelta(days=365)

# Find customers with no orders in the last year
inactive_customers = Customer.objects.filter(
    orders__isnull=True
) | Customer.objects.filter(
    orders__order_date__lt=one_year_ago
).distinct()

count = inactive_customers.count()
inactive_customers.delete()

# Log the results
with open('/tmp/customer_cleanup_log.txt', 'a') as f:
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f.write(f"[{timestamp}] Deleted {count} inactive customers\n")
PYTHON_EOF
