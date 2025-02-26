import os
import sqlite3
import pandas as pd

# Define base directory dynamically
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define file paths dynamically
csv_file_path = os.path.join(BASE_DIR, "data", "ecommerce_data.csv")
db_file_path = os.path.join(BASE_DIR, "data", "ecommerce.db")

# Connect to SQLite database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Check if CSV exists
if not os.path.exists(csv_file_path):
    print(f"Error: CSV file not found at {csv_file_path}")
    exit(1)

# Load CSV into Pandas DataFrame
df = pd.read_csv(csv_file_path)

# Create table if it does not exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS purchases (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id INTEGER,
        category TEXT,
        price REAL,
        quantity INTEGER,
        purchase_date TEXT
    )
''')

# Insert data into the database
df.to_sql("purchases", conn, if_exists="replace", index=False)
print("Data inserted into purchases table successfully!")

# Commit and close
conn.commit()
conn.close()
