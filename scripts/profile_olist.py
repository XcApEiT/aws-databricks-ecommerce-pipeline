#!/usr/bin/env python3
import argparse, csv, json
from pathlib import Path

EXPECTED = [
    "olist_customers_dataset.csv", "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv", "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv", "olist_orders_dataset.csv",
    "olist_products_dataset.csv", "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
]

def profile(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        rows = sum(1 for _ in reader)
    return {"file": path.name, "rows": rows, "columns": columns}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {"files": [], "missing_files": []}
    for filename in EXPECTED:
        path = args.input_dir / filename
        if path.exists():
            result["files"].append(profile(path))
        else:
            result["missing_files"].append(filename)
    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
