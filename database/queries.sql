-- Sample KPI Queries for MySQL Database Approach

-- 1. Repeat Customers (customers with more than one order)
SELECT 
    c.customer_id,
    c.customer_name,
    c.mobile_number,
    c.region,
    COUNT(DISTINCT o.order_id) AS order_count
FROM customers c
INNER JOIN orders o ON c.mobile_number = o.mobile_number
GROUP BY c.customer_id, c.customer_name, c.mobile_number, c.region
HAVING order_count > 1
ORDER BY order_count DESC, c.mobile_number;

-- 2. Monthly Order Trends
SELECT 
    DATE_FORMAT(order_date_time, '%Y-%m-01') AS order_month,
    COUNT(DISTINCT order_id) AS order_count
FROM orders
GROUP BY order_month
ORDER BY order_month;

-- 3. Regional Revenue
SELECT 
    COALESCE(c.region, 'Unknown') AS region,
    SUM(o.total_amount) AS revenue
FROM orders o
LEFT JOIN customers c ON o.mobile_number = c.mobile_number
GROUP BY region
ORDER BY revenue DESC;

-- 4. Top Spenders (Last 30 Days)
SELECT 
    o.mobile_number,
    SUM(o.total_amount) AS total_spend,
    c.customer_id,
    c.customer_name,
    c.region
FROM orders o
LEFT JOIN customers c ON o.mobile_number = c.mobile_number
WHERE o.order_date_time >= DATE_SUB(
    (SELECT MAX(order_date_time) FROM orders), 
    INTERVAL 30 DAY
)
GROUP BY o.mobile_number, c.customer_id, c.customer_name, c.region
ORDER BY total_spend DESC
LIMIT 10;
