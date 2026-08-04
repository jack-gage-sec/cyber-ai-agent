import random
from datetime import datetime, timedelta

import pandas as pd

from synthetic_data.shared_entities import EMPLOYEES, HOSTS


SEVERITIES = [
    "Low",
    "Medium",
    "High",
    "Critical",
]

ALERT_TYPES = [
    "Malware Detection",
    "Failed Login",
    "Privilege Escalation",
    "Data Exfiltration",
    "Suspicious PowerShell",
    "Ransomware Activity",
    "Credential Dumping",
]

MITRE_ATTACKS = [
    "T1059",
    "T1003",
    "T1078",
    "T1041",
    "T1021",
    "T1486",
    "T1562",
]


def generate_alerts(num_records=50000):

    alerts = []

    for i in range(num_records):

        employee = random.choice(EMPLOYEES)
        host = random.choice(HOSTS)

        timestamp = (
            datetime.now()
            - timedelta(
                days=random.randint(0, 90),
                minutes=random.randint(0, 1440),
            )
        )

        alerts.append(
            {
                "alert_id": f"ALT{i+1:06}",
                "timestamp": timestamp,
                "employee_id": employee["employee_id"],
                "hostname": host["hostname"],
                "severity": random.choice(SEVERITIES),
                "alert_type": random.choice(ALERT_TYPES),
                "mitre_attack": random.choice(MITRE_ATTACKS),
                "source_ip": host["ip_address"],
                "destination_ip": f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
                "description": f"{random.choice(ALERT_TYPES)} detected on {host['hostname']}"
            }
        )

    return pd.DataFrame(alerts)