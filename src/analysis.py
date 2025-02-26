import os
import sqlite3
import pandas as pd

# Define base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database path
db_file_path = os.path.join(BASE_DIR, "data", "ecommerce.db")
report_dir = os.path.join(BASE_DIR, "reports")
report_path = os.path.join(report_dir, "insights.txt")

# Ensure the reports directory exists
os.makedirs(report_dir, exist_ok=True)

# Connect to database
conn = sqlite3.connect(db_file_path)

# Query: Get top 5 best-selling products
top_products = pd.read_sql("""
    SELECT product_id, category, SUM(quantity) AS total_sold
    FROM purchases_cleaned
    GROUP BY product_id, category
    ORDER BY total_sold DESC
    LIMIT 5
""", conn)

# Query: Calculate total revenue per day
daily_revenue = pd.read_sql("""
    SELECT purchase_date, SUM(price * quantity) AS total_revenue
    FROM purchases_cleaned
    GROUP BY purchase_date
    ORDER BY purchase_date
""", conn)

# Ensure directory exists before writing
with open(report_path, "w") as file:
    file.write("Top 5 Best-Selling Products:\n")
    file.write(top_products.to_string(index=False))
    file.write("\n\nDaily Revenue:\n")
    file.write(daily_revenue.to_string(index=False))

print("Analysis completed. Insights saved to reports/insights.txt")

conn.close()
