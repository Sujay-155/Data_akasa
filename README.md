

## Requirements
- Python 3.13 or higher
- pandas, lxml, python-dotenv, schedule, mysql-connector-python
- MySQL Server (for database approach)

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

# Database Configuration (for MySQL approach)
DB_HOST=localhost
DB_PORT=3306
DB_NAME=akasa_data
DB_USER=root
DB_PASSWORD=your_password
```

For MySQL approach, ensure MySQL server is running and accessible.

## Usage

### In-Memory Approach (Python/Pandas)

Run pipeline manually:
```bash
py run_pipeline.py
```

Run scheduled pipeline (daily at 1:00 AM):
```bash
py run_scheduler.py
```

### Database Approach (MySQL)

Run database pipeline:
```bash
py run_db_pipeline.py
```

This will:
1. Create database tables
2. Load CSV/XML data into MySQL
3. Execute SQL queries for KPIs
4. Save results to `output/db_*.csv` files

## Outputs

In-memory approach reports:
- `kpi_repeat_customers.csv` - Customers with multiple orders
- `kpi_monthly_trends.csv` - Order counts by month
- `kpi_regional_revenue.csv` - Revenue by region
- `kpi_top_spenders_last_30_days.csv` - Top spenders (last 30 days)

Database approach reports (prefixed with `db_`):
- `db_repeat_customers.csv`
- `db_monthly_trends.csv`
- `db_regional_revenue.csv`
- `db_top_spenders_last_30_days.csv`

## Data Files

Place raw data in `data/raw/`:
- `task_DE_new_customers.csv` - Customer information (CSV)
- `task_DE_new_orders.xml` - Order transactions (XML)

## Features

- Loads CSV and XML data
- Two implementation approaches (in-memory and database)
- Cleans and validates data
- Handles missing values and duplicates
- Timezone-aware processing (Asia/Kolkata)
- Generates 4 KPI reports
- Daily scheduled execution at 1:00 AM (in-memory)
- SQL-based analytics with MySQL
