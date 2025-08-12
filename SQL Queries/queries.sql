USE ecommerce;

-- 1. Top 5 products by revenue (What sells the most money-wise?)
SELECT p.name, SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status <> 'Cancelled'
GROUP BY p.product_id
ORDER BY revenue DESC
LIMIT 5;

-- 2. Monthly revenue trend (How much money we made each month)
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, SUM(total_amount) AS revenue
FROM orders
WHERE status <> 'Cancelled'
GROUP BY month
ORDER BY month;

-- 3. Average Order Value (AOV) (How much a typical customer spends per order)
SELECT AVG(total_amount) AS AOV FROM orders WHERE status <> 'Cancelled';


-- 4. Best customer by lifetime value (total money spent)
SELECT c.customer_id, CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
       SUM(o.total_amount) AS lifetime_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status <> 'Cancelled'
GROUP BY c.customer_id
ORDER BY lifetime_value DESC
LIMIT 1;

-- 5. Revenue by category
SELECT p.category, SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status <> 'Cancelled'
GROUP BY p.category
ORDER BY revenue DESC;

-- 6. Percentage of orders cancelled
SELECT 
    CONCAT(ROUND(SUM(CASE WHEN status='Cancelled' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2), '%') AS cancelled_percentage
FROM orders;

-- 7. Top country by number of customers
SELECT country, COUNT(*) AS total_customers
FROM customers
GROUP BY country
ORDER BY total_customers DESC
LIMIT 1;

-- 8. Average number of items per order
SELECT ROUND(AVG(item_count), 2) AS avg_items_per_order
FROM (
    SELECT o.order_id, COUNT(oi.order_item_id) AS item_count
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_id
) t;


