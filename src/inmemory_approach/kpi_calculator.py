"""
In-Memory Approach - KPI Calculations
Calculate KPIs using pandas dataframes
"""
import pandas as pd


def get_repeat_customers(orders: pd.DataFrame, customers: pd.DataFrame = None) -> pd.DataFrame:
    """Identify customers with more than one order"""
    counts = orders.groupby('mobile_number')['order_id'].nunique().reset_index(name='order_count')
    repeats = counts[counts['order_count'] > 1]
    
    if customers is not None:
        repeats = repeats.merge(customers, on='mobile_number', how='left')
    
    return repeats.sort_values(['order_count', 'mobile_number'], ascending=[False, True]).reset_index(drop=True)


def get_monthly_trends(orders: pd.DataFrame, tz: str) -> pd.DataFrame:
    """Aggregate orders by month"""
    local_ts = orders['order_date_time'].dt.tz_convert(tz).dt.tz_localize(None)
    orders = orders.assign(order_month=local_ts.dt.to_period('M').dt.to_timestamp())
    
    return (
        orders.groupby('order_month')['order_id']
        .nunique()
        .reset_index(name='order_count')
        .sort_values('order_month')
        .reset_index(drop=True)
    )


def get_regional_revenue(orders: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """Calculate total revenue by region"""
    merged = orders.merge(customers[['mobile_number', 'region']], on='mobile_number', how='left')
    merged['region'] = merged['region'].fillna('Unknown')
    
    return (
        merged.groupby('region', dropna=False)['total_amount']
        .sum()
        .reset_index(name='revenue')
        .sort_values('revenue', ascending=False)
        .reset_index(drop=True)
    )


def get_top_spenders_last_30_days(
    orders: pd.DataFrame,
    customers: pd.DataFrame,
    tz: str,
    top_n: int = 10
) -> pd.DataFrame:
    """Rank customers by spend in last 30 days"""
    now_utc = orders['order_date_time'].max()
    if pd.isna(now_utc):
        return pd.DataFrame(columns=['mobile_number', 'total_spend', 'customer_id', 'customer_name', 'region'])
    
    cutoff_utc = (now_utc.tz_convert(tz) - pd.Timedelta(days=30)).tz_convert('UTC')
    recent = orders[orders['order_date_time'] >= cutoff_utc]
    
    spend = recent.groupby('mobile_number')['total_amount'].sum().reset_index(name='total_spend')
    result = spend.merge(customers, on='mobile_number', how='left')
    
    return result.sort_values('total_spend', ascending=False).head(top_n).reset_index(drop=True)
