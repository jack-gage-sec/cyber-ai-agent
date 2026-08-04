'''from faker import Faker
import numpy as np

fake = Faker()

Faker.seed(42)
np.random.seed(42)'''

import os
import sys

from pathlib import Path

dir_above_cep = Path(__file__).resolve().parents[2]
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), dir_above_cep))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)


from pathlib import Path
import pandas as pd

from synthetic_data.users import generate_users
from synthetic_data.hosts import generate_hosts
from synthetic_data.alerts import generate_alerts
from synthetic_data.access_reviews import generate_access_reviews
from synthetic_data.policy_exceptions import generate_policy_exceptions
from synthetic_data.control_tests import generate_control_tests

OUTPUT_DIR = Path("synthetic_data/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def save(df, filename):
    path = OUTPUT_DIR / filename
    df.to_csv(path, index=False)
    print(f"Created {path} ({len(df)} rows)")

if __name__ == "__main__":
    print("Generating synthetic datasets...")

    save(generate_users(), "users.csv")
    save(generate_hosts(), "hosts.csv")
    save(generate_alerts(50000), "alerts.csv")
    save(generate_access_reviews(5000), "access_reviews.csv")
    save(generate_policy_exceptions(1000), "policy_exceptions.csv")
    save(generate_control_tests(1000), "control_tests.csv")

    print("Done!")
