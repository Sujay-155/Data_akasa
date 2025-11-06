
import sys
from pathlib import Path

import pandas as pd

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.config import CONFIG
from utils.logger import setup_logger
from inmemory_approach.data_loader import load_customers, load_orders, clean_customers, clean_orders
from inmemory_approach.kpi_calculator import (
    get_repeat_customers,
    get_monthly_trends,
    get_regional_revenue,
    get_top_spenders_last_30_days
)

log = setup_logger('akasa')


def ensure_dir(path: Path):
    """Create directory if it doesn't exist"""
    path.mkdir(parents=True, exist_ok=True)


def save_report(df: pd.DataFrame, reports_dir: str, filename: str):
    """Save dataframe as CSV report"""
    ensure_dir(Path(reports_dir))
    outpath = Path(reports_dir) / filename
    df.to_csv(outpath, index=False)
    log.info(f"Saved report: {outpath}")


def main():
    """Main pipeline execution"""
    log.info("Starting Akasa Air - In-memory (pandas) pipeline")
    
    # 1. Load raw data
    try:
        customers_raw = load_customers(CONFIG['CUSTOMERS_CSV'])
        orders_raw = load_orders(CONFIG['ORDERS_XML'])
    except FileNotFoundError as e:
        log.error(f"File not found: {e}")
        sys.exit(1)
    except Exception as e:
        log.error(f"Error loading data: {e}")
        sys.exit(1)
    
    # 2. Clean and validate
    customers = clean_customers(customers_raw)
    orders = clean_orders(orders_raw, tz=CONFIG['TZ'])
    
    log.info(f"Customers after cleaning: {len(customers)} rows")
    log.info(f"Orders after cleaning: {len(orders)} rows")
    
    # 3. Calculate KPIs
    log.info("Calculating KPIs...")
    repeat_customers = get_repeat_customers(orders, customers)
    monthly_trends = get_monthly_trends(orders, tz=CONFIG['TZ'])
    regional_revenue = get_regional_revenue(orders, customers)
    top_spenders = get_top_spenders_last_30_days(
        orders, customers, tz=CONFIG['TZ'], top_n=CONFIG['TOP_N']
    )
    
    # 4. Save reports
    log.info("Saving reports...")
    save_report(repeat_customers, CONFIG['REPORTS_DIR'], 'kpi_repeat_customers.csv')
    save_report(monthly_trends, CONFIG['REPORTS_DIR'], 'kpi_monthly_trends.csv')
    save_report(regional_revenue, CONFIG['REPORTS_DIR'], 'kpi_regional_revenue.csv')
    save_report(top_spenders, CONFIG['REPORTS_DIR'], 'kpi_top_spenders_last_30_days.csv')
    
    # 5. Display results
    pd.set_option('display.width', 120)
    pd.set_option('display.max_columns', 20)
    
    print("\n" + "=" * 80)
    print("KPI RESULTS")
    print("=" * 80)
    
    print("\n--- Repeat Customers ---")
    print(repeat_customers.to_string(index=False))
    
    print("\n--- Monthly Order Trends ---")
    print(monthly_trends.to_string(index=False))
    
    print("\n--- Regional Revenue ---")
    print(regional_revenue.to_string(index=False))
    
    print("\n--- Top Spenders (Last 30 Days) ---")
    print(top_spenders.to_string(index=False))
    
    print("\n" + "=" * 80)
    log.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()
