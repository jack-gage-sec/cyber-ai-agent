import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "D:\Backup Files\Experiments\Compliance Evidence Pipeline"))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

import datetime

from sqlalchemy import text

from database.connection import engine


def check_database():

    try:

        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

        return {
            "status": "healthy",
            "message": "PostgreSQL Connected",
        }


    except Exception as e:

        return {
            "status": "error",
            "message": str(e),
        }



def get_timestamp():

    return datetime.datetime.now()