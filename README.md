
## Requirements
- Python 3.13 or higher
- pandas, lxml, python-dotenv, schedule

## Setup

Install dependencies:
```bash
py -m pip install -r requirements.txt
```

Configure `.env` file:
```
TZ=Asia/Kolkata
CUSTOMERS_CSV=data/raw/task_DE_new_customers.csv
ORDERS_XML=data/raw/task_DE_new_orders.xml
REPORTS_DIR=output
TOP_N=10
```

## Usage

### Run pipeline manually
```bash
py run_pipeline.py
```

### Run scheduled pipeline (daily at 1:00 AM)
```bash
py run_scheduler.py
```

Press Ctrl+C to stop the scheduler.

## Outputs

Reports saved to `output/`:
- `repeat_customers.csv` - Customers with multiple orders
- `monthly_trends.csv` - Order counts by month
- `regional_revenue.csv` - Revenue by region
- `top_spenders_last_30_days.csv` - Top spenders (last 30 days)

## Data Files

Place raw data in `data/raw/`:
- `task_DE_new_customers.csv` - Customer information (CSV)
- `task_DE_new_orders.xml` - Order transactions (XML)

## Features

- Loads CSV and XML data
- Cleans and validates data
- Handles missing values and duplicates
- Timezone-aware processing (Asia/Kolkata)
- Generates 4 KPI reports
- Daily scheduled execution at 1:00 AM
