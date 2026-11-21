# Setup and cost notes

1. Download Olist from Kaggle and extract into `data/raw/`.
2. Run `python scripts/profile_olist.py --input-dir data/raw`.
3. Configure an encrypted, private S3 bucket and least-privilege IAM role.
4. Configure Databricks S3 access through an IAM role and supported Unity Catalog storage credential/external location.
5. Pass paths as job parameters; do not hardcode credentials.

No infrastructure is applied automatically. AWS, Databricks compute, and Redshift may incur charges. Start with local profiling, set budgets, and terminate compute when not in use.
