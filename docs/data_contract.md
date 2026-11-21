# Olist source contract

Source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Nine source CSVs and their grains:
| File | Grain / key |
|---|---|
| orders | one row/order; `order_id` |
| customers | one order-specific customer row; `customer_id`; use `customer_unique_id` for repeat people |
| order_items | one row/order item; `(order_id, order_item_id)` |
| order_payments | one row/payment sequence; `(order_id, payment_sequential)` |
| order_reviews | review grain; profile `review_id` uniqueness |
| products | one row/product; `product_id` |
| sellers | one row/seller; `seller_id` |
| geolocation | many coordinate observations per ZIP prefix; no unique ZIP key |
| category translation | one row/category; `product_category_name` |

Modeling hazards:
- An order may have multiple items, payments, and review records.
- Joining payment and item facts before aggregation causes fan-out and inflated sums.
- `customer_id` is not a person-level repeat-customer key.
- Aggregate geolocation to ZIP before joining to customers/sellers.
- Preserve misspelled source headers such as `product_name_lenght` in Bronze; normalize in Silver.
- Lifecycle timestamps may be null depending on order status.

Profile actual downloaded CSVs; reference row counts are not proof of local completeness.
