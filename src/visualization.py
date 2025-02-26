import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database path
db_file_path = os.path.join(BASE_DIR, "data", "ecommerce.db")

# Connect to database
conn = sqlite3.connect(db_file_path)

# Load revenue data
df = pd.read_sql("""
    SELECT purchase_date, SUM(price * quantity) AS total_revenue
    FROM purchases_cleaned
    GROUP BY purchase_date
""", conn)

conn.close()

# Convert purchase_date to datetime
df["purchase_date"] = pd.to_datetime(df["purchase_date"])

# Plot revenue trends
plt.figure(figsize=(10, 5))
sns.lineplot(data=df, x="purchase_date", y="total_revenue", marker="o", color="b")
plt.title("Daily Revenue Over Time")
plt.xlabel("Purchase Date")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()
