from faker import Faker
import pymysql, random, datetime
from tqdm import trange

fake = Faker()

# Database config
HOST = "127.0.0.1"
PORT = 3306
USER = "root"
PASSWORD = "root"
DB = "ecommerce"

# Connect
conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DB, autocommit=False)
cur = conn.cursor()

def rand_date(days_back=800):
    start = datetime.date.today() - datetime.timedelta(days=days_back)
    return start + datetime.timedelta(days=random.randint(0, days_back))

# Customers
customers = []
for _ in range(200):
    fn = fake.first_name()
    ln = fake.last_name()
    email = f"{fn.lower()}.{ln.lower()}{random.randint(1,999)}@example.com"
    country = fake.country()
    customers.append((fn, ln, email, country, rand_date(1200)))
cur.executemany("INSERT INTO customers (first_name, last_name, email, country, created_at) VALUES (%s,%s,%s,%s,%s)", customers)
conn.commit()

# Products
categories = ["Electronics","Home","Sports","Clothing","Stationery"]
products = []
for _ in range(100):
    name = fake.word().title() + " " + random.choice(["Pro","Max","Mini","X"])
    cat = random.choice(categories)
    price = round(random.uniform(100, 5000), 2)
    products.append((name, cat, price, rand_date(1000)))
cur.executemany("INSERT INTO products (name, category, price, created_at) VALUES (%s,%s,%s,%s)", products)
conn.commit()

# Fetch prices
cur.execute("SELECT product_id, price FROM products")
price_map = {pid: p for pid, p in cur.fetchall()}

# Orders
statuses = ["Placed","Shipped","Delivered","Cancelled"]
payment_methods = ["Credit Card","UPI","Net Banking","Cash"]

for _ in trange(2000, desc="Orders"):
    cust_id = random.randint(1, 200)
    order_date = rand_date()
    status = random.choice(statuses)
    num_items = random.randint(1, 4)
    total = 0
    items = []
    for _ in range(num_items):
        pid = random.choice(list(price_map.keys()))
        qty = random.randint(1, 3)
        price = price_map[pid]
        total += qty * price
        items.append((pid, qty, price))
    cur.execute("INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES (%s,%s,%s,%s)", (cust_id, order_date, status, round(total,2)))
    oid = cur.lastrowid
    cur.executemany("INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s,%s,%s,%s)", [(oid, pid, qty, price) for pid, qty, price in items])
    pay_amt = 0 if status=="Cancelled" else round(total,2)
    cur.execute("INSERT INTO payments (order_id, payment_method, amount, payment_date) VALUES (%s,%s,%s,%s)", (oid, random.choice(payment_methods), pay_amt, order_date))
    
conn.commit()
conn.close()
