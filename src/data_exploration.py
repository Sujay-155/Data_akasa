import pandas as pd
import xml.etree.ElementTree as ET
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_customers_csv(file_path):
    """Load customers data from CSV file"""
    print("=" * 80)
    print("LOADING CUSTOMERS DATA (CSV)")
    print("=" * 80)
    
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded {len(df)} customer records\n")
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

def load_orders_xml(file_path):
    """Load orders data from XML file"""
    print("=" * 80)
    print("LOADING ORDERS DATA (XML)")
    print("=" * 80)
    
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        orders_data = []
        for order in root.findall('.//order'):
            order_dict = {}
            for child in order:
                order_dict[child.tag] = child.text
            orders_data.append(order_dict)
        
        df = pd.DataFrame(orders_data)
        print(f"Successfully loaded {len(df)} order records\n")
        return df
    except Exception as e:
        print(f"Error loading XML: {e}")
        return None

def display_dataset_info(df, dataset_name):
    """Display comprehensive information about a dataset"""
    print("\n" + "=" * 80)
    print(f"{dataset_name.upper()} - DATASET ANALYSIS")
    print("=" * 80)
    
    # 1. HEAD - First 5 rows
    print(f"\nHEAD - First 5 rows of {dataset_name}:")
    print("-" * 80)
    print(df.head())
    
    # 2. MISSING VALUES
    print(f"\nMISSING VALUES in {dataset_name}:")
    print("-" * 80)
    missing_values = df.isnull().sum()
    
    missing_df = pd.DataFrame({
        'Column': missing_values.index,
        'Missing Count': missing_values.values
    })
    
    print(missing_df.to_string(index=False))
    
    total_missing = missing_values.sum()
    if total_missing == 0:
        print(f"\nNo missing values found in {dataset_name}")
    else:
        print(f"\nTotal missing values: {total_missing}")
    
    # 3. BASIC STATISTICS
    print(f"\nBASIC STATISTICS for {dataset_name}:")
    print("-" * 80)
    print(f"Total Rows: {len(df)}")
    print(f"Total Columns: {len(df.columns)}")
    print(f"Duplicate Rows: {df.duplicated().sum()}")

def main():
    """Main execution function"""
    # Get the workspace root directory
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # File paths
    customers_file = os.path.join(workspace_root, 'data', 'raw', 'task_DE_new_customers.csv')
    orders_file = os.path.join(workspace_root, 'data', 'raw', 'task_DE_new_orders.xml')
    
    # Check if files exist
    print("Checking for data files...")
    print(f"Customers CSV: {customers_file}")
    print(f"Orders XML: {orders_file}\n")
    
    if not os.path.exists(customers_file):
        print(f"Error: Customers file not found at {customers_file}")
        return
    
    if not os.path.exists(orders_file):
        print(f"Error: Orders file not found at {orders_file}")
        return
    
    # Load datasets
    customers_df = load_customers_csv(customers_file)
    orders_df = load_orders_xml(orders_file)
    
    # Display information for customers
    if customers_df is not None:
        display_dataset_info(customers_df, "CUSTOMERS")
    
    # Display information for orders
    if orders_df is not None:
        display_dataset_info(orders_df, "ORDERS")
    
    # Summary
    print("\n" + "=" * 80)
    print("EXPLORATION SUMMARY")
    print("=" * 80)
    
    if customers_df is not None and orders_df is not None:
        print(f"Customers loaded: {len(customers_df)} records")
        print(f"Orders loaded: {len(orders_df)} records")
    
    print("\n" + "=" * 80)
    print("Exploration completed successfully")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
