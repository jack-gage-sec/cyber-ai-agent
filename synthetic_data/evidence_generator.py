import os
import random

from faker import Faker

fake = Faker()

EVIDENCE_DIRECTORY = "D:\Backup Files\Experiments\Compliance Evidence Pipeline\Compliance-AI\policies"

POLICY_TEMPLATES = {

    "Access Control Policy": """
Access Control Policy

Purpose:
Ensure users only receive access required for their job responsibilities.

Control Requirements:

- User access must be approved.
- Privileged access must be reviewed quarterly.
- Terminated employees must have access removed.

Evidence Requirements:

- Access review reports
- Approval records
- Identity management logs

Control Owner:
Security Engineering

Review Frequency:
Quarterly
""",


    "Incident Response Policy": """
Incident Response Policy

Purpose:
Define procedures for identifying, containing, and recovering from security incidents.

Requirements:

- Security incidents must be documented.
- Critical incidents require escalation.
- Post-incident reviews must be completed.

Evidence:

- Incident tickets
- Investigation reports
- Lessons learned documentation

Control Owner:
Security Operations
""",


    "Configuration Management Policy": """
Configuration Management Policy

Purpose:
Maintain secure configurations across enterprise systems.

Requirements:

- Systems must use approved baselines.
- Unauthorized changes must be investigated.
- Vulnerability remediation must be tracked.

Evidence:

- Configuration scans
- Vulnerability reports
- Change tickets

Control Owner:
Infrastructure Engineering
"""
}


def generate_control_evidence(control_tests):

    evidence_directory = "../policies/control_evidence"

    os.makedirs(
        evidence_directory,
        exist_ok=True
    )


    for _, row in control_tests.iterrows():

        filename = (
            f"{row['evidence_id']}.txt"
        )


        filepath = os.path.join(
            evidence_directory,
            filename
        )


        document = f"""
Control Evidence Report

Evidence ID:
{row['evidence_id']}


Control:
{row['control_id']}


Description:
{row['control_description']}


Framework:
{row['framework']}


Test Result:
{row['result']}


Finding:
{row['finding']}


Tester:
{row['tester']}


Test Date:
{row['test_date']}


This evidence record was generated
for compliance testing purposes.
"""


        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(document)


def generate_policy_documents():

    policy_directory = "../policies"

    os.makedirs(
        policy_directory,
        exist_ok=True
    )


    for name, content in POLICY_TEMPLATES.items():

        filename = (
            name.replace(
                " ",
                "_"
            )
            + ".txt"
        )


        filepath = os.path.join(
            policy_directory,
            filename
        )


        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content)


def generate_evidence(control_tests):

    generate_policy_documents()

    generate_control_evidence(
        control_tests
    )