import os
import sys

from pathlib import Path

dir_above_cep = Path(__file__).resolve().parents[2]
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), dir_above_cep))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)


"""
Compliance-AI ETL Pipeline

Loads all synthetic compliance datasets into PostgreSQL
in dependency order.
"""

from pathlib import Path

from ingestion.batch_loader import load_csv
from pipelines.etl_pipeline import transform
from pipelines.data_quality import (
    check_duplicate_ids,
    check_record_count,
)
from database.loaders import load_dataframe


# --------------------------------------------------------
# Project paths
# --------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = (
    BASE_DIR /
    "synthetic_data" /
    "output"
)


# --------------------------------------------------------
# Generic dataset processor
# --------------------------------------------------------

def process_dataset(
    filename,
    table_name,
    primary_key,
):

    print("\n" + "=" * 60)
    print(f"Processing {table_name}")
    print("=" * 60)

    file_path = DATA_DIR / filename

    print(f"Loading file: {file_path}")

    df = load_csv(file_path)

    print(f"Loaded {len(df)} records")

    df = transform(df)

    check_record_count(df)

    check_duplicate_ids(
        df,
        primary_key,
    )

    print("Columns:")
    print(df.columns.tolist())

    load_dataframe(
        df,
        table_name,
    )

    print(f"{table_name} loaded successfully")


# --------------------------------------------------------
# Main pipeline
# --------------------------------------------------------

def run_pipeline():

    # Parent tables first

    process_dataset(
        "users.csv",
        "users",
        "employee_id",
    )

    process_dataset(
        "hosts.csv",
        "hosts",
        "hostname",
    )

    # Child tables

    process_dataset(
        "alerts.csv",
        "alerts",
        "alert_id",
    )

    process_dataset(
        "access_reviews.csv",
        "access_reviews",
        "review_id",
    )

    process_dataset(
        "policy_exceptions.csv",
        "policy_exceptions",
        "exception_id",
    )

    process_dataset(
        "control_tests.csv",
        "control_tests",
        "test_id",
    )

    print("\nPipeline completed successfully.")


# --------------------------------------------------------

if __name__ == "__main__":
    run_pipeline()
