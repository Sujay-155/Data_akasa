"""
Database Data Loader
Loads CSV and XML data into MySQL database
"""
import pandas as pd
import mysql.connector
from mysql.connector import Error
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.config import CONFIG, DB_CONFIG
from utils.logger import setup_logger

logger = setup_logger(__name__)


def create_database_if_not_exists():
    """Create database if it doesn't exist"""
    try:
        config = DB_CONFIG.copy()
        db_name = config.pop('database')
        
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.close()
        conn.close()
        logger.info(f"Database '{db_name}' ready")
    except Error as e:
        logger.error(f"Database creation failed: {e}")
        raise


def get_connection():
    """Create MySQL database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        logger.error(f"Database connection failed: {e}")
        raise


def create_tables(conn):
    """Create database tables using schema file"""
    schema_file = Path(__file__).resolve().parent.parent.parent / 'database' / 'schema.sql'
    
    try:
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        cursor = conn.cursor()
        for statement in schema_sql.split(';'):
            if statement.strip():
                cursor.execute(statement)
        conn.commit()
        logger.info("Database tables created successfully")
    except Error as e:
        logger.error(f"Failed to create tables: {e}")
        raise


def load_customers_to_db(conn, csv_path):
    """Load customers from CSV to database"""
    df = pd.read_csv(csv_path, dtype=str)
    df = df.fillna('')
    df['mobile_number'] = df['mobile_number'].astype('string')
    
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO customers (customer_id, customer_name, mobile_number, region)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            customer_name = VALUES(customer_name),
            region = VALUES(region)
    """
    
    for _, row in df.iterrows():
        cursor.execute(insert_query, (
            row['customer_id'],
            row['customer_name'] or 'Unknown',
            row['mobile_number'],
            row['region'] or 'Unknown'
        ))
    
    conn.commit()
    logger.info(f"Loaded {len(df)} customers into database")


def load_orders_to_db(conn, xml_path):
    """Load orders from XML to database"""
    df = pd.read_xml(xml_path)
    
    # Convert mobile_number properly
    df['mobile_number'] = df['mobile_number'].astype('Int64').astype('string')
    
    # Convert numeric fields
    df['sku_count'] = pd.to_numeric(df['sku_count'], errors='coerce').fillna(0).astype('int64')
    df['total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce').fillna(0.0)
    
    # Parse datetime
    df['order_date_time'] = pd.to_datetime(df['order_date_time'], errors='coerce')
    
    # Remove invalid rows
    df = df.dropna(subset=['order_id', 'mobile_number', 'order_date_time'])
    df = df.drop_duplicates(subset=['order_id'], keep='first')
    
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO orders (order_id, mobile_number, sku_count, total_amount, order_date_time)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            sku_count = VALUES(sku_count),
            total_amount = VALUES(total_amount)
    """
    
    for _, row in df.iterrows():
        cursor.execute(insert_query, (
            row['order_id'],
            row['mobile_number'],
            int(row['sku_count']),
            float(row['total_amount']),
            row['order_date_time']
        ))
    
    conn.commit()
    logger.info(f"Loaded {len(df)} orders into database")


def main():
    """Main execution for database loading"""
    try:
        logger.info("Starting database load process")
        
        create_database_if_not_exists()
        
        conn = get_connection()
        logger.info("Connected to MySQL database")
        
        create_tables(conn)
        
        load_customers_to_db(conn, CONFIG['CUSTOMERS_CSV'])
        load_orders_to_db(conn, CONFIG['ORDERS_XML'])
        
        conn.close()
        logger.info("Database load completed successfully")
        
    except Exception as e:
        logger.error(f"Database load failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
