import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# DB Config
HOST = "127.0.0.1"
PORT = 3306
USER = "root"
PASSWORD = "root"
DB = "ecommerce"

# Connect
conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DB)

# 1. Monthly Revenue Trend
monthly_query = """
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, SUM(total_amount) AS revenue
FROM orders
WHERE status <> 'Cancelled'
GROUP BY month
ORDER BY month;
"""
monthly_df = pd.read_sql(monthly_query, conn)

plt.figure(figsize=(10,5))
sns.lineplot(data=monthly_df, x="month", y="revenue", marker="o")
plt.xticks(rotation=45)
plt.title("Monthly Revenue Trend")
plt.ylabel("Revenue")
plt.xlabel("Month")
plt.tight_layout()
plt.show()

# 2. Top 5 Products by Revenue
top_products_query = """
SELECT p.name, SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status <> 'Cancelled'
GROUP BY p.product_id
ORDER BY revenue DESC
LIMIT 5;
"""
top_products_df = pd.read_sql(top_products_query, conn)

plt.figure(figsize=(8,5))
sns.barplot(data=top_products_df, x="revenue", y="name", palette="viridis")
plt.title("Top 5 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")
plt.tight_layout()
plt.show()

# 3. Revenue by Category
category_query = """
SELECT p.category, SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status <> 'Cancelled'
GROUP BY p.category
ORDER BY revenue DESC;
"""
category_df = pd.read_sql(category_query, conn)

plt.figure(figsize=(7,5))
sns.barplot(data=category_df, x="category", y="revenue", palette="coolwarm")
plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()

conn.close()
