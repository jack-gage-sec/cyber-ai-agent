import random
from datetime import datetime, timedelta

import pandas as pd

from synthetic_data.shared_entities import EMPLOYEES


POLICIES = [
    "Password Policy",
    "MFA Policy",
    "Remote Access Policy",
    "Acceptable Use Policy",
    "Patch Management Policy",
]

RISK_LEVELS = [
    "Low",
    "Medium",
    "High",
    "Critical",
]


def generate_policy_exceptions(num_records=1000):

    exceptions = []

    for i in range(num_records):

        employee = random.choice(EMPLOYEES)

        created = (
            datetime.now()
            - timedelta(days=random.randint(0, 180))
        )

        expiration = (
            created
            + timedelta(days=random.randint(30, 365))
        )

        exceptions.append(
            {
                "exception_id": f"PEX{i+1:06}",
                "policy": random.choice(POLICIES),
                "owner_employee_id": employee["employee_id"],
                "owner_name": employee["name"],
                "department": employee["department"],
                "risk_level": random.choice(RISK_LEVELS),
                "justification": "Business requirement",
                "approved": random.choice([True, False]),
                "created_date": created,
                "expiration_date": expiration,
            }
        )

    return pd.DataFrame(exceptions)