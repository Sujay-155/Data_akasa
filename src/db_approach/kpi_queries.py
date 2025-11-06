"""
KPI Calculation using SQL Queries
Executes SQL queries to calculate business metrics
"""
import pandas as pd
import mysql.connector
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.config import CONFIG, DB_CONFIG
from utils.logger import setup_logger

logger = setup_logger(__name__)


def get_connection():
    """Create MySQL database connection"""
    return mysql.connector.connect(**DB_CONFIG)


def get_repeat_customers(conn):
    """KPI 1: Customers with more than one order"""
    query = """
        SELECT 
            c.customer_id,
            c.customer_name,
            c.mobile_number,
            c.region,
            COUNT(DISTINCT o.order_id) AS order_count
        FROM customers c
        INNER JOIN orders o ON c.mobile_number = o.mobile_number
        GROUP BY c.customer_id, c.customer_name, c.mobile_number, c.region
        HAVING order_count > 1
        ORDER BY order_count DESC, c.mobile_number
    """
    return pd.read_sql(query, conn)


def get_monthly_trends(conn):
    """KPI 2: Monthly order trends"""
    query = """
        SELECT 
            DATE_FORMAT(order_date_time, '%Y-%m-01') AS order_month,
            COUNT(DISTINCT order_id) AS order_count
        FROM orders
        GROUP BY order_month
        ORDER BY order_month
    """
    df = pd.read_sql(query, conn)
    df['order_month'] = pd.to_datetime(df['order_month'])
    return df


def get_regional_revenue(conn):
    """KPI 3: Revenue by region"""
    query = """
        SELECT 
            COALESCE(c.region, 'Unknown') AS region,
            SUM(o.total_amount) AS revenue
        FROM orders o
        LEFT JOIN customers c ON o.mobile_number = c.mobile_number
        GROUP BY region
        ORDER BY revenue DESC
    """
    return pd.read_sql(query, conn)


def get_top_spenders_last_30_days(conn, top_n=10):
    """KPI 4: Top spenders in last 30 days (parameterized LIMIT)."""
    query = """
        SELECT 
            o.mobile_number,
            SUM(o.total_amount) AS total_spend,
            c.customer_id,
            c.customer_name,
            c.region
        FROM orders o
        LEFT JOIN customers c ON o.mobile_number = c.mobile_number
        WHERE o.order_date_time >= DATE_SUB(
            (SELECT MAX(order_date_time) FROM orders), 
            INTERVAL 30 DAY
        )
        GROUP BY o.mobile_number, c.customer_id, c.customer_name, c.region
        ORDER BY total_spend DESC
        LIMIT %s
    """
    return pd.read_sql(query, conn, params=[int(top_n)])


def calculate_all_kpis(conn, top_n=10):
    """Calculate all KPIs and return as dictionary"""
    logger.info("Calculating KPIs from database")
    
    kpis = {
        'repeat_customers': get_repeat_customers(conn),
        'monthly_trends': get_monthly_trends(conn),
        'regional_revenue': get_regional_revenue(conn),
        'top_spenders_last_30_days': get_top_spenders_last_30_days(conn, top_n)
    }
    
    logger.info("All KPIs calculated successfully")
    return kpis
