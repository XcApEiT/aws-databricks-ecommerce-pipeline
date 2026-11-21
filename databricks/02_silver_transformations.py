# Databricks notebook source
from pyspark.sql import functions as F

dbutils.widgets.text("OLIST_DELTA_PATH", "")
root = dbutils.widgets.get("OLIST_DELTA_PATH").rstrip("/")
if not root: raise ValueError("Set OLIST_DELTA_PATH")

def read(name): return spark.read.format("delta").load(f"{root}/bronze/{name}")
def write(df, name):
    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{root}/silver/{name}")

orders = read("orders")
for c in ["order_purchase_timestamp","order_approved_at","order_delivered_carrier_date","order_delivered_customer_date","order_estimated_delivery_date"]:
    orders = orders.withColumn(c, F.to_timestamp(F.col(c)))
orders = orders.withColumn("order_status", F.lower(F.trim("order_status"))).dropDuplicates(["order_id"])
write(orders, "orders")

customers = read("customers").dropDuplicates(["customer_id"])
write(customers, "customers")

items = read("order_items")
items = (items.withColumn("order_item_id", F.col("order_item_id").cast("int"))
         .withColumn("price", F.col("price").cast("decimal(12,2)"))
         .withColumn("freight_value", F.col("freight_value").cast("decimal(12,2)"))
         .dropDuplicates(["order_id","order_item_id"]))
write(items, "order_items")

payments = read("order_payments")
payments = (payments.withColumn("payment_sequential", F.col("payment_sequential").cast("int"))
            .withColumn("payment_installments", F.col("payment_installments").cast("int"))
            .withColumn("payment_value", F.col("payment_value").cast("decimal(12,2)"))
            .dropDuplicates(["order_id","payment_sequential"]))
write(payments, "order_payments")

reviews = read("order_reviews").withColumn("review_score", F.col("review_score").cast("int"))
write(reviews.dropDuplicates(["review_id"]), "order_reviews")
products = read("products")
for c in ["product_name_lenght","product_description_lenght","product_photos_qty","product_weight_g","product_length_cm","product_height_cm","product_width_cm"]:
    if c in products.columns: products = products.withColumn(c, F.col(c).cast("int"))
write(products.dropDuplicates(["product_id"]), "products")
write(read("sellers").dropDuplicates(["seller_id"]), "sellers")
write(read("category_translation").dropDuplicates(["product_category_name"]), "category_translation")

# Avoid joining raw geolocation: repeated ZIP observations would fan out rows.
geo = read("geolocation").withColumn("geolocation_lat", F.col("geolocation_lat").cast("double")).withColumn("geolocation_lng", F.col("geolocation_lng").cast("double"))
geo_zip = geo.groupBy("geolocation_zip_code_prefix").agg(F.avg("geolocation_lat").alias("avg_latitude"), F.avg("geolocation_lng").alias("avg_longitude"), F.count("*").alias("observation_count"))
write(geo_zip, "geolocation_by_zip")
