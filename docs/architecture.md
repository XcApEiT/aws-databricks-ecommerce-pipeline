# Architecture

1. Source: nine Olist CSV files from Kaggle.
2. S3 raw: immutable landing files.
3. Bronze: source-aligned Delta tables with ingestion metadata.
4. Silver: typed, cleaned, deduplicated, quality-checked tables.
5. Gold: analytics-ready dimensions and facts.
6. Optional Redshift serving layer.

Proposed Gold model:
- Dimensions: `dim_customer`, `dim_product`, `dim_seller`, `dim_date`.
- Facts: `fact_order_item` at order-item grain, `fact_payment` at payment-sequence grain, and `fact_review` at review grain.
- Keep payment/review facts separate from item fact to avoid multiplying amounts and review scores.
- Define order-status eligibility before publishing AOV or late-delivery KPIs.
- GMV proxy: sum item `price`; report `freight_value` separately.
