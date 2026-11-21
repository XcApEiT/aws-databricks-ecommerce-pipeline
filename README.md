# Olist E-Commerce Lakehouse | AWS + Databricks

Portfolio data-engineering project using the Olist Brazilian E-Commerce Public Dataset.

**Status:** Phase 1 scaffold only. No AWS resources, Databricks jobs, or Redshift warehouse have been deployed or validated.

## Architecture
`Kaggle CSVs -> S3 raw -> Databricks/PySpark -> Delta Bronze -> Silver -> Gold -> optional Redshift`

## Dataset
Download from https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce and extract the nine CSVs into `data/raw/`. Raw data is excluded from Git. Kaggle lists the dataset under CC BY-NC-SA 4.0; review terms before redistribution.

## Local setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python scripts/profile_olist.py --input-dir data/raw
pytest -q
```

## Databricks sequence
1. Upload CSVs to S3 raw prefix.
2. Configure secure S3 access with an IAM role / supported Unity Catalog storage credential.
3. Set `OLIST_RAW_PATH` and `OLIST_DELTA_PATH` job parameters.
4. Run `databricks/01_bronze_ingestion.py`, `02_silver_transformations.py`, then `03_gold_model.py`.
5. Validate data before loading optional Redshift serving tables.

## Progress
- [x] Project scope and initial code scaffold
- [x] Source contract and local profiler
- [ ] Download and profile all nine files
- [ ] Validate S3 landing and IAM
- [ ] Validate Databricks Bronze
- [ ] Validate Silver quality rules
- [ ] Validate Gold star schema
- [ ] Optional Redshift serving layer
- [ ] End-to-end run and cost review

AWS, Databricks, and Redshift can incur charges. Never commit credentials, raw data, Terraform state, or real `.tfvars`.
