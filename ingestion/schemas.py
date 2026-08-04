"""
Data schemas for Compliance-AI ingestion.

Used to validate incoming security and compliance data.
"""


ALERT_SCHEMA = [
    "alert_id",
    "timestamp",
    "employee_id",
    "hostname",
    "severity",
    "alert_type",
    "mitre_attack",
    "source_ip",
    "destination_ip",
]


ACCESS_REVIEW_SCHEMA = [
    "review_id",
    "employee_id",
    "employee_name",
    "department",
    "system",
    "access_level",
    "reviewer",
    "approved",
    "review_date",
]


POLICY_EXCEPTION_SCHEMA = [
    "exception_id",
    "policy",
    "owner_employee_id",
    "owner_name",
    "department",
    "risk_level",
    "justification",
    "approved",
    "created_date",
    "expiration_date",
]


CONTROL_TEST_SCHEMA = [
    "test_id",
    "control_id",
    "control_description",
    "framework",
    "result",
    "evidence_id",
    "tester",
    "test_date",
    "finding",
]


USER_SCHEMA = [
    "employee_id",
    "name",
    "department",
    "job_title",
    "privilege",
]


HOST_SCHEMA = [
    "hostname",
    "ip_address",
    "operating_system",
    "criticality",
]