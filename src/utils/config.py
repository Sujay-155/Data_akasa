"""
Configuration Management
Loads environment variables and provides application settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
OUTPUT_DIR = BASE_DIR / 'output'
LOGS_DIR = BASE_DIR / 'logs'

# Application Configuration
CONFIG = {
    'TZ': os.getenv('TZ', 'Asia/Kolkata'),
    'CUSTOMERS_CSV': os.getenv('CUSTOMERS_CSV', str(RAW_DATA_DIR / 'task_DE_new_customers.csv')),
    'ORDERS_XML': os.getenv('ORDERS_XML', str(RAW_DATA_DIR / 'task_DE_new_orders.xml')),
    'REPORTS_DIR': os.getenv('REPORTS_DIR', str(OUTPUT_DIR)),
    'TOP_N': int(os.getenv('TOP_N', '10')),
}

# Database Configuration (for future use)
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'database': os.getenv('DB_NAME', 'akasa_data'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '')
}
