"""
Batch ingestion loader.

Loads compliance and security artifacts
from CSV/JSON files.
"""

import os
import pandas as pd
from datetime import datetime



def load_csv(filepath):

    print(
        f"Loading CSV: {filepath}"
    )

    df = pd.read_csv(filepath)

    return add_metadata(
        df,
        filepath
    )



def load_json(filepath):

    print(
        f"Loading JSON: {filepath}"
    )

    df = pd.read_json(filepath)

    return add_metadata(
        df,
        filepath
    )



def add_metadata(df, filepath):

    df["source_file"] = (
        os.path.basename(str(filepath))
    )

    df["ingested_at"] = (
        datetime.utcnow()
    )

    df["data_classification"] = (
        classify_data(filepath)
    )

    return df



def classify_data(filepath):

    filename = (
        str(filepath)
        .lower()
    )

    if (
        "user" in filename
        or "access" in filename
    ):
        return "Confidential"


    if (
        "alert" in filename
        or "vulnerability" in filename
    ):
        return "Internal-Security"


    if "policy" in filename:
        return "Internal"


    return "Internal"