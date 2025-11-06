"""
Database Approach - Main Pipeline
Load data to MySQL, calculate KPIs, and generate reports
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db_approach.load_data import get_connection, create_database_if_not_exists, create_tables, load_customers_to_db, load_orders_to_db
from db_approach.kpi_queries import calculate_all_kpis
from utils.config import CONFIG
from utils.logger import setup_logger

logger = setup_logger(__name__)


def save_reports(kpis, output_dir):
    """Save KPI results to CSV files"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    reports = {
        'db_repeat_customers.csv': kpis['repeat_customers'],
        'db_monthly_trends.csv': kpis['monthly_trends'],
        'db_regional_revenue.csv': kpis['regional_revenue'],
        'db_top_spenders_last_30_days.csv': kpis['top_spenders_last_30_days']
    }
    
    for filename, df in reports.items():
        filepath = output_path / filename
        df.to_csv(filepath, index=False)
        logger.info(f"Saved report: {filepath}")


def display_results(kpis):
    """Display KPI results in console"""
    print("\n" + "="*80)
    print("DATABASE APPROACH - KPI RESULTS")
    print("="*80)
    
    print("\n--- Repeat Customers ---")
    print(kpis['repeat_customers'].to_string(index=False))
    
    print("\n--- Monthly Order Trends ---")
    print(kpis['monthly_trends'].to_string(index=False))
    
    print("\n--- Regional Revenue ---")
    print(kpis['regional_revenue'].to_string(index=False))
    
    print("\n--- Top Spenders (Last 30 Days) ---")
    print(kpis['top_spenders_last_30_days'].to_string(index=False))
    
    print("\n" + "="*80)


def main():
    """Execute complete database pipeline"""
    try:
        logger.info("Starting Akasa Air - Database (MySQL) pipeline")
        
        # Create database if not exists
        create_database_if_not_exists()
        
        # Connect to database
        conn = get_connection()
        logger.info("Connected to MySQL database")
        
        # Create tables
        create_tables(conn)
        
        # Load data
        logger.info("Loading data into database...")
        load_customers_to_db(conn, CONFIG['CUSTOMERS_CSV'])
        load_orders_to_db(conn, CONFIG['ORDERS_XML'])
        
        # Calculate KPIs
        kpis = calculate_all_kpis(conn, top_n=CONFIG['TOP_N'])
        
        # Close connection
        conn.close()
        
        # Save reports
        save_reports(kpis, CONFIG['REPORTS_DIR'])
        
        # Display results
        display_results(kpis)
        
        logger.info("Database pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"Database pipeline failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
