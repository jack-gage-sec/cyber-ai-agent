"""
Database queries used by AI agents.
"""

import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "D:\Backup Files\Experiments\Compliance Evidence Pipeline"))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

from sqlalchemy import text

from database.connection import SessionLocal


def get_access_reviews():

    db = SessionLocal()

    results = db.execute(
        text(
            """
            SELECT *
            FROM access_reviews
            LIMIT 100;
            """
        )
    )

    data = [
        dict(row._mapping)
        for row in results
    ]

    db.close()

    return data



def get_policy_exceptions():

    db = SessionLocal()

    results = db.execute(
        text(
            """
            SELECT *
            FROM policy_exceptions
            LIMIT 100;
            """
        )
    )

    data = [
        dict(row._mapping)
        for row in results
    ]

    db.close()

    return data

def get_control(control_id):

    db = SessionLocal()

    result = db.execute(
        text(
            """
            SELECT *
            FROM controls
            WHERE control_id = :id
            """
        ),
        {
            "id": control_id
        }
    )

    row = result.fetchone()

    db.close()

    if row:
        return dict(row._mapping)

    return None

def get_audit_logs():
    from database.connection import SessionLocal
    from database.models import AuditLog

    db = SessionLocal()

    try:
        return db.query(AuditLog).all()
    finally:
        db.close()

def get_control_tests():
    from database.connection import SessionLocal
    from database.models import ControlTest

    db = SessionLocal()

    try:
        return db.query(ControlTest).all()
    finally:
        db.close()