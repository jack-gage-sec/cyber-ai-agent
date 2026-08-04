"""
Shared constants used by the Compliance-AI synthetic data generators.

Keeping enterprise values here prevents duplication and makes it
easy to add new systems, policies, controls, and alert types later.
"""

# ==========================================================
# Organization
# ==========================================================

DEPARTMENTS = [
    "Engineering",
    "Finance",
    "Human Resources",
    "Information Technology",
    "Legal",
    "Sales",
    "Security",
]

JOB_TITLES = [
    "Analyst",
    "Engineer",
    "Senior Engineer",
    "Administrator",
    "Manager",
    "Director",
]

PRIVILEGES = [
    "Standard",
    "Elevated",
    "Administrator",
]

# Probability of each privilege level
PRIVILEGE_WEIGHTS = [
    0.85,
    0.10,
    0.05,
]

# ==========================================================
# Assets
# ==========================================================

OPERATING_SYSTEMS = [
    "Windows 11",
    "Windows Server 2022",
    "Ubuntu 24.04",
    "Red Hat Enterprise Linux 9",
]

CRITICALITY_LEVELS = [
    "Low",
    "Medium",
    "High",
    "Critical",
]

CRITICALITY_WEIGHTS = [
    0.40,
    0.35,
    0.20,
    0.05,
]

# ==========================================================
# Vulnerabilities
# ==========================================================

CVES = [
    ("CVE-2025-10001", 9.8),
    ("CVE-2025-10002", 8.2),
    ("CVE-2025-10003", 7.5),
    ("CVE-2025-10004", 6.4),
    ("CVE-2025-10005", 5.6),
    ("CVE-2025-10006", 4.1),
]

VULNERABILITY_STATUS = [
    "Open",
    "Patched",
]

VULNERABILITY_STATUS_WEIGHTS = [
    0.70,
    0.30,
]

# ==========================================================
# SIEM Alerts
# ==========================================================

ALERT_TYPES = [
    "Multiple Failed Logins",
    "Malware Detected",
    "Impossible Travel Login",
    "Privilege Escalation",
    "Suspicious PowerShell Activity",
    "Data Exfiltration Attempt",
    "Unauthorized USB Device",
    "Ransomware Behavior",
]

MITRE_ATTACK_MAPPING = {
    "Multiple Failed Logins": "T1110",
    "Malware Detected": "T1204",
    "Impossible Travel Login": "T1078",
    "Privilege Escalation": "T1068",
    "Suspicious PowerShell Activity": "T1059.001",
    "Data Exfiltration Attempt": "T1041",
    "Unauthorized USB Device": "T1091",
    "Ransomware Behavior": "T1486",
}

SEVERITIES = [
    "Low",
    "Medium",
    "High",
    "Critical",
]

SEVERITY_WEIGHTS = [
    0.50,
    0.30,
    0.15,
    0.05,
]

# ==========================================================
# Access Reviews
# ==========================================================

SYSTEMS = [
    "AWS",
    "Azure",
    "GitHub",
    "ServiceNow",
    "Salesforce",
    "Active Directory",
    "Microsoft 365",
    "Jira",
]

ACCESS_LEVELS = [
    "Read",
    "Write",
    "Administrator",
]

ACCESS_LEVEL_WEIGHTS = [
    0.60,
    0.30,
    0.10,
]

REVIEWERS = [
    "Security Team",
    "IT Operations",
    "Internal Audit",
    "Compliance Team",
]

# ==========================================================
# Policy Exceptions
# ==========================================================

POLICIES = [
    "Access Control Policy",
    "Password Policy",
    "Encryption Standard",
    "Logging Policy",
    "Vendor Management Policy",
    "Incident Response Policy",
]

RISK_LEVELS = [
    "Low",
    "Medium",
    "High",
]

JUSTIFICATIONS = [
    "Legacy application compatibility",
    "Business requirement",
    "Temporary operational need",
    "Vendor limitation",
    "Migration in progress",
]

# ==========================================================
# Control Testing
# ==========================================================

FRAMEWORKS = [
    "SOC 2",
    "NIST CSF",
    "NIST SP 800-53",
    "ISO 27001",
]

CONTROL_IDS = [
    "AC-01",
    "AC-02",
    "AC-03",
    "CM-01",
    "CM-02",
    "CM-03",
    "IA-01",
    "IA-02",
    "IR-01",
    "IR-02",
]

CONTROL_RESULTS = [
    "PASS",
    "FAIL",
]

CONTROL_RESULT_WEIGHTS = [
    0.85,
    0.15,
]

TESTERS = [
    "Internal Audit",
    "Compliance Team",
    "Security Engineering",
]

FINDINGS = [
    "Control operating effectively.",
    "Minor documentation issue identified.",
    "Evidence incomplete.",
    "Inactive accounts detected.",
    "Privileged access review overdue.",
    "No issues identified.",
]

# ==========================================================
# Evidence
# ==========================================================

EVIDENCE_TYPES = [
    "Access Review",
    "Vulnerability Scan",
    "Firewall Review",
    "Control Test",
    "Risk Assessment",
]