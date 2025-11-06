import sys
import os
import time
import schedule
from datetime import datetime

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from inmemory_approach.main import main
from utils.logger import setup_logger

logger = setup_logger(__name__)

def job():
    """Execute the pipeline and handle errors"""
    try:
        logger.info("=" * 60)
        logger.info(f"Scheduled run started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        main()
        logger.info("Scheduled run completed successfully")
    except Exception as e:
        logger.error(f"Scheduled run failed: {e}", exc_info=True)

def main_scheduler():
    """Schedule daily pipeline execution at 1:00 AM"""
    schedule.every().day.at("01:00").do(job)
    
    logger.info("Scheduler started - pipeline will run daily at 1:00 AM")
    logger.info("Press Ctrl+C to stop")
    
    # Run immediately on startup (optional - comment out if not needed)
    logger.info("Running initial execution...")
    job()
    
    # Keep running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")

if __name__ == "__main__":
    main_scheduler()
