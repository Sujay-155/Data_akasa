"""
In-Memory Approach - Data Loading
Load and clean CSV and XML files using pandas
"""
import pandas as pd
import logging

log = logging.getLogger('akasa')


def load_customers(path: str) -> pd.DataFrame:
    """
    Load customers from CSV file
    Expected columns: customer_id, customer_name, mobile_number, region
    """
    log.info(f"Loading customers CSV: {path}")
    df = pd.read_csv(
        path,
        dtype={
            'customer_id': 'string',
            'customer_name': 'string',
            'mobile_number': 'string',
            'region': 'string',
        },
        keep_default_na=False
    )
    # Ensure mobile_number is string (handle cases where CSV has it as number)
    df['mobile_number'] = df['mobile_number'].astype('string')
    log.info(f"Customers loaded: {len(df)} rows")
    return df


def load_orders(path: str) -> pd.DataFrame:
    """
    Load orders from XML file
    Expected fields: order_id, mobile_number, order_date_time, sku_id, sku_count, total_amount
    """
    log.info(f"Loading orders XML: {path}")
    df = pd.read_xml(path)
    
    # Validate expected columns
    expected = {'order_id', 'mobile_number', 'order_date_time', 'sku_id', 'sku_count', 'total_amount'}
    missing = expected.difference(df.columns)
    if missing:
        raise ValueError(f"Orders XML missing columns: {sorted(missing)}")
    
    # Basic type conversions
    df['order_id'] = df['order_id'].astype('string')
    # Convert mobile_number from float to int first, then to string (removes .0)
    df['mobile_number'] = df['mobile_number'].astype('Int64').astype('string')
    df['sku_id'] = df['sku_id'].astype('string')
    
    log.info(f"Orders loaded: {len(df)} rows")
    return df


def _trim_string_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Trim whitespace from string columns"""
    for col in df.select_dtypes(include=['string', 'object']).columns:
        df[col] = df[col].astype('string').str.strip()
    return df


def _parse_datetime_series(s: pd.Series, tz: str) -> pd.Series:
    """Parse datetime and normalize to UTC"""
    dt = pd.to_datetime(s, errors='coerce')
    if dt.dt.tz is None:
        dt = dt.dt.tz_localize(tz, ambiguous='infer')
    return dt.dt.tz_convert('UTC')


def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate customer data
    - Trim whitespace
    - Standardize region names
    - Handle duplicates
    - Fill missing values
    """
    df = df.copy()
    df = _trim_string_cols(df)
    
    # Standardize region
    if 'region' in df.columns:
        df['region'] = df['region'].fillna('').astype('string').str.strip()
        df['region'] = df['region'].replace('', 'Unknown')
        df['region'] = df['region'].str.title()
    
    # Handle duplicate mobile numbers
    dupes = df['mobile_number'].duplicated(keep=False)
    if dupes.any():
        log.warning("Duplicate mobile_number found in customers; keeping first occurrence")
        df = df.drop_duplicates(subset=['mobile_number'], keep='first')
    
    # Fill missing values
    df['customer_id'] = df['customer_id'].fillna(pd.NA).astype('string')
    df['customer_name'] = df['customer_name'].fillna('Unknown').astype('string')
    
    return df.reset_index(drop=True)


def clean_orders(df: pd.DataFrame, tz: str) -> pd.DataFrame:
    """
    Clean and validate order data
    - Trim whitespace
    - Convert numeric types
    - Parse and normalize timestamps
    - Drop invalid rows
    - Handle duplicates
    """
    df = df.copy()
    df = _trim_string_cols(df)
    
    # Convert numeric columns
    df['sku_count'] = pd.to_numeric(df['sku_count'], errors='coerce')
    df['total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce')
    
    # Parse timestamps and normalize to UTC
    df['order_date_time'] = _parse_datetime_series(df['order_date_time'], tz)
    
    # Drop rows with critical missing data
    before = len(df)
    df = df.dropna(subset=['order_id', 'mobile_number', 'order_date_time'])
    after = len(df)
    dropped = before - after
    if dropped > 0:
        log.warning(f"Dropped {dropped} orders with missing id/mobile/timestamp")
    
    # Handle duplicate order IDs
    if df['order_id'].duplicated().any():
        log.warning("Duplicate order_id detected; keeping first occurrence")
        df = df.drop_duplicates(subset=['order_id'], keep='first')
    
    # Fill remaining NaN values
    df['sku_count'] = df['sku_count'].fillna(0).astype('int64')
    df['total_amount'] = df['total_amount'].fillna(0.0).astype('float64')
    
    return df.reset_index(drop=True)
