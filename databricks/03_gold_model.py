# Databricks notebook source
from pyspark.sql import functions as F

dbutils.widgets.text("OLIST_DELTA_PATH", "")
root = dbutils.widgets.get("OLIST_DELTA_PATH").rstrip("/")
if not root: raise ValueError("Set OLIST_DELTA_PATH")
def silver(name): return spark.read.format("delta").load(f"{root}/silver/{name}")
def save(df, name):
    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{root}/gold/{name}")

customers, products, sellers = silver("customers"), silver("products"), silver("sellers")
orders, items = silver("orders"), silver("order_items")
translations = silver("category_translation")

save(customers.select("customer_id","customer_unique_id","customer_zip_code_prefix","customer_city","customer_state"), "dim_customer")
dim_product = products.join(translations, "product_category_name", "left")
save(dim_product, "dim_product")
save(sellers.select("seller_id","seller_zip_code_prefix","seller_city","seller_state"), "dim_seller")

fact_item = (items.join(orders.select("order_id","customer_id","order_status","order_purchase_timestamp","order_delivered_customer_date","order_estimated_delivery_date"), "order_id", "left")
 .join(dim_product.select("product_id","product_category_name","product_category_name_english"), "product_id", "left")
 .join(sellers.select("seller_id"), "seller_id", "left")
 .withColumn("purchase_date", F.to_date("order_purchase_timestamp"))
 .withColumn("is_late_delivery", F.when(F.col("order_delivered_customer_date").isNull(), F.lit(None)).otherwise(F.col("order_delivered_customer_date") > F.col("order_estimated_delivery_date"))))
save(fact_item, "fact_order_item")
# Separate grains prevent item x payment x review fan-out.
save(silver("order_payments"), "fact_payment")
save(silver("order_reviews"), "fact_review")
