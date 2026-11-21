# Databricks notebook source
from pyspark.sql import functions as F

dbutils.widgets.text("OLIST_RAW_PATH", "")
dbutils.widgets.text("OLIST_DELTA_PATH", "")
raw = dbutils.widgets.get("OLIST_RAW_PATH").rstrip("/")
delta = dbutils.widgets.get("OLIST_DELTA_PATH").rstrip("/")
if not raw or not delta:
    raise ValueError("Set OLIST_RAW_PATH and OLIST_DELTA_PATH")

sources = {
 "customers":"olist_customers_dataset.csv",
 "geolocation":"olist_geolocation_dataset.csv",
 "order_items":"olist_order_items_dataset.csv",
 "order_payments":"olist_order_payments_dataset.csv",
 "order_reviews":"olist_order_reviews_dataset.csv",
 "orders":"olist_orders_dataset.csv",
 "products":"olist_products_dataset.csv",
 "sellers":"olist_sellers_dataset.csv",
 "category_translation":"product_category_name_translation.csv"
}
for table, filename in sources.items():
    df = (spark.read.option("header", True).option("inferSchema", False)
          .option("mode", "PERMISSIVE").csv(f"{raw}/{filename}")
          .withColumn("_source_file", F.lit(filename))
          .withColumn("_ingested_at", F.current_timestamp()))
    (df.write.format("delta").mode("overwrite").option("overwriteSchema", "true")
       .save(f"{delta}/bronze/{table}"))
    print("Bronze written:", table)
