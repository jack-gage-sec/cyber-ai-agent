import os
import sys

from pathlib import Path

dir_above_cep = Path(__file__).resolve().parents[2]
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), dir_above_cep))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

import pandas as pd

from sqlalchemy import text

from database.connection import engine


def load_dataframe(table, limit=None):

    if limit:

        query = text(
            f"""
            SELECT *
            FROM {table}
            LIMIT {limit}
            """
        )

    else:

        query = text(
            f"""
            SELECT *
            FROM {table}
            """
        )

    return pd.read_sql(
        query,
        engine,
    )
