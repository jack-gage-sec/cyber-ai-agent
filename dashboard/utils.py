import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "D:\Backup Files\Experiments\Compliance Evidence Pipeline"))

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