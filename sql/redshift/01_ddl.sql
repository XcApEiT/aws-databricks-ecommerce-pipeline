-- Optional serving layer; load Gold data before querying.
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE TABLE IF NOT EXISTS analytics.fact_order_item (
 order_id VARCHAR(64), order_item_id INTEGER, product_id VARCHAR(64),
 seller_id VARCHAR(64), customer_id VARCHAR(64), order_status VARCHAR(32),
 purchase_date DATE, price DECIMAL(12,2), freight_value DECIMAL(12,2),
 is_late_delivery BOOLEAN
);
