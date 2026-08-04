import random
from datetime import datetime, timedelta

import pandas as pd

from synthetic_data.shared_entities import EMPLOYEES


SYSTEMS = [
    "Active Directory",
    "GitHub",
    "AWS",
    "Azure",
    "Salesforce",
    "ServiceNow",
]

ACCESS_LEVELS = [
    "Read",
    "Write",
    "Admin",
]

REVIEWERS = [
    "Alice Johnson",
    "Bob Smith",
    "Carol Davis",
    "David Brown",
]


def generate_access_reviews(num_records=5000):

    reviews = []

    for i in range(num_records):

        employee = random.choice(EMPLOYEES)

        reviews.append(
            {
                "review_id": f"AR{i+1:06}",
                "employee_id": employee["employee_id"],
                "employee_name": employee["name"],
                "department": employee["department"],
                "system": random.choice(SYSTEMS),
                "access_level": random.choice(ACCESS_LEVELS),
                "reviewer": random.choice(REVIEWERS),
                "approved": random.choice([True, False]),
                "review_date": datetime.now()
                - timedelta(days=random.randint(0, 365)),
            }
        )

    return pd.DataFrame(reviews)