import os
import sqlite3
import pandas as pd

# Define base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database path
db_file_path = os.path.join(BASE_DIR, "data", "ecommerce.db")

# Connect to SQLite database
conn = sqlite3.connect(db_file_path)

# Load data from database
df = pd.read_sql("SELECT * FROM purchases", conn)

# Convert `purchase_date` to datetime format
df["purchase_date"] = pd.to_datetime(df["purchase_date"], errors="coerce")

# Remove rows with invalid dates
df = df.dropna(subset=["purchase_date"])

# Remove duplicates
df.drop_duplicates(inplace=True)

# Handle missing values
df.fillna({"category": "Unknown"}, inplace=True)

# Update cleaned data back to the database
df.to_sql("purchases_cleaned", conn, if_exists="replace", index=False)

print("Data cleaning completed successfully!")

conn.commit()
conn.close()
