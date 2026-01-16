import pandas as pd
from sqlalchemy import create_engine

db_password = 'admin123'
db_name = 'ecommerce_db'
db_user = 'postgres'
db_host = 'localhost'
db_port = 5432

csv_folder_path = './'

# Create connection str
connection_str = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(connection_str)

def load_data(file_name, table_name):
    print(f"Loading {file_name} into {table_name}...")

    df = pd.read_csv(f"./{file_name}")

    for col in df.columns:
        if 'date' in col or 'timestamp' in col:
            df[col] = pd.to_datetime(df[col])

    try:
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"✅ Success! Loaded {len(df)} rows into {table_name}.")
    except Exception as e:
        print(f"❌ Error loading {table_name}: {e}")  

files_to_load = {
    'olist_customers_dataset.csv': 'customers',
    'olist_orders_dataset.csv': 'orders',
    'olist_order_items_dataset.csv': 'order_items',
    'olist_order_payments_dataset.csv': 'order_payments'
}

for csv_file, table_name in files_to_load.items():
    load_data(csv_file, table_name)

print("\nETL Job Complete!")