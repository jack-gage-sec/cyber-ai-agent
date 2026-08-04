"""
Shared entities used across all synthetic data generators.

This ensures referential integrity between datasets.
"""

import random

from faker import Faker

fake = Faker()

NUM_EMPLOYEES = 500
NUM_HOSTS = 200


# =====================================================
# Employees
# =====================================================

EMPLOYEES = []

for i in range(1, NUM_EMPLOYEES + 1):

    EMPLOYEES.append(
        {
            "employee_id": f"EMP{i:05}",
            "name": fake.name(),
            "department": random.choice(
                [
                    "Engineering",
                    "Security",
                    "Finance",
                    "Human Resources",
                    "Legal",
                    "Operations",
                    "IT",
                ]
            ),
            "job_title": random.choice(
                [
                    "Analyst",
                    "Engineer",
                    "Administrator",
                    "Manager",
                    "Director",
                ]
            ),
            "privilege": random.choice(
                [
                    "User",
                    "Power User",
                    "Administrator",
                ]
            ),
        }
    )


# =====================================================
# Hosts
# =====================================================

HOSTS = []

for i in range(1, NUM_HOSTS + 1):

    owner = random.choice(EMPLOYEES)

    HOSTS.append(
        {
            "hostname": f"HOST{i:04}",
            "ip_address": fake.ipv4_private(),
            "operating_system": random.choice(
                [
                    "Windows 11",
                    "Windows Server 2022",
                    "Ubuntu 24.04",
                    "RHEL 9",
                ]
            ),
            "criticality": random.choice(
                [
                    "Low",
                    "Medium",
                    "High",
                    "Critical",
                ]
            ),
            "owner_employee_id": owner["employee_id"],
        }
    )