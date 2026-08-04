import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "D:\Backup Files\Experiments\Compliance Evidence Pipeline"))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

from database.connection import SessionLocal
from database.models import Control


db = SessionLocal()


controls = [

    Control(
        control_id="AC-001",
        name="Access Reviews",
        description=(
            "Ensure user access is reviewed "
            "periodically."
        ),
        policy_id="AC-001",
        evidence_sources=(
            "access_reviews,"
            "policy_exceptions"
        ),
    ),


    Control(
        control_id="IR-001",
        name="Incident Response",
        description=(
            "Ensure security incidents "
            "are detected and handled."
        ),
        policy_id="IR-001",
        evidence_sources=(
            "alerts"
        ),
    ),


    Control(
        control_id="VM-001",
        name="Vulnerability Management",
        description=(
            "Ensure vulnerabilities are "
            "identified and remediated."
        ),
        policy_id="VM-001",
        evidence_sources=(
            "vulnerability_scans"
        ),
    ),

]


db.add_all(controls)

db.commit()

db.close()


print(
    "Controls loaded."
)