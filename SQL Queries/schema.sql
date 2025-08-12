CREATE DATABASE ecommerce;
USE ecommerce;

   CREATE TABLE customers (
       customer_id INT AUTO_INCREMENT PRIMARY KEY,
       first_name VARCHAR(50),
       last_name VARCHAR(50),
       email VARCHAR(100) UNIQUE,
       country VARCHAR(50),
       created_at DATE
   );

   CREATE TABLE products (
       product_id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100),
       category VARCHAR(50),
       price DECIMAL(10,2),
       created_at DATE
   );

   CREATE TABLE orders (
       order_id INT AUTO_INCREMENT PRIMARY KEY,
       customer_id INT,
       order_date DATE,
       status ENUM('Placed','Shipped','Delivered','Cancelled'),
       total_amount DECIMAL(10,2),
       FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
   );

   CREATE TABLE order_items (
       order_item_id INT AUTO_INCREMENT PRIMARY KEY,
       order_id INT,
       product_id INT,
       quantity INT,
       unit_price DECIMAL(10,2),
       FOREIGN KEY (order_id) REFERENCES orders(order_id),
       FOREIGN KEY (product_id) REFERENCES products(product_id)
   );

   CREATE TABLE payments (
       payment_id INT AUTO_INCREMENT PRIMARY KEY,
       order_id INT,
       payment_method VARCHAR(50),
       amount DECIMAL(10,2),
       payment_date DATE,
       FOREIGN KEY (order_id) REFERENCES orders(order_id)
   );

   CREATE TABLE monthly_reports (
       report_id INT AUTO_INCREMENT PRIMARY KEY,
       report_month VARCHAR(7),
       total_revenue DECIMAL(15,2),
       total_orders INT,
       top_product VARCHAR(100),
       generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

show tables;
SELECT COUNT(*) FROM orders;
