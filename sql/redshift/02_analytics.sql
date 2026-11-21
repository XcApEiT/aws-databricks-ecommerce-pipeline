-- Monthly item revenue and freight; item grain, count orders distinctly.
SELECT DATE_TRUNC('month', purchase_date) AS month,
       SUM(price) AS item_revenue_brl,
       SUM(freight_value) AS freight_brl,
       COUNT(DISTINCT order_id) AS orders
FROM analytics.fact_order_item
WHERE purchase_date IS NOT NULL
GROUP BY 1 ORDER BY 1;

-- Late-delivery rate; count distinct orders, not item rows.
SELECT 100.0 * COUNT(DISTINCT CASE WHEN is_late_delivery THEN order_id END)
       / NULLIF(COUNT(DISTINCT CASE WHEN is_late_delivery IS NOT NULL THEN order_id END),0)
       AS late_delivery_pct
FROM analytics.fact_order_item;
