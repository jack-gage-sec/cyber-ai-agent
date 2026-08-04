"""
Compliance AI Dashboard
"""

import os
import sys
from pathlib import Path

dir_above_cep = Path(__file__).resolve().parents[2]
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), dir_above_cep))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

import streamlit as st

from dashboard.components.header import show_header
from dashboard.components.sidebar import show_sidebar
from dashboard.components.metric_cards import show_metrics

from dashboard.utils import load_dataframe

from dashboard.charts import (
    alerts_by_severity,
    alerts_by_mitre,
)

from dashboard.components.login import login

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Compliance AI",
    page_icon="🛡️",
    layout="wide",
)

if "user" not in st.session_state:

    login()

    st.stop()

# ---------------------------------------------------
# Logged-in User Display (Step 4)
# ---------------------------------------------------

st.sidebar.write(
    f"""
    Logged in:
    {st.session_state.user['username']}

    Role:
    {st.session_state.user['role']}
    """
)

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

MAX_ALERTS = 5000

alerts = load_dataframe(
    "alerts",
    limit=MAX_ALERTS,
)

exceptions = load_dataframe(
    "policy_exceptions"
)

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

show_sidebar()

st.sidebar.header("Alert Filters")

severity_filter = st.sidebar.multiselect(
    "Severity",
    sorted(alerts["severity"].dropna().unique()),
)

alert_filter = st.sidebar.multiselect(
    "Alert Type",
    sorted(alerts["alert_type"].dropna().unique()),
)

mitre_filter = st.sidebar.multiselect(
    "MITRE ATT&CK",
    sorted(alerts["mitre_attack"].dropna().unique()),
)

employee_search = st.sidebar.text_input(
    "Employee ID",
)

hostname_search = st.sidebar.text_input(
    "Hostname",
)

filtered_alerts = alerts.copy()

if severity_filter:

    filtered_alerts = filtered_alerts[
        filtered_alerts["severity"].isin(
            severity_filter
        )
    ]

if alert_filter:

    filtered_alerts = filtered_alerts[
        filtered_alerts["alert_type"].isin(
            alert_filter
        )
    ]

if mitre_filter:

    filtered_alerts = filtered_alerts[
        filtered_alerts["mitre_attack"].isin(
            mitre_filter
        )
    ]

if employee_search:

    filtered_alerts = filtered_alerts[
        filtered_alerts["employee_id"]
        .str.contains(
            employee_search,
            case=False,
            na=False,
        )
    ]

if hostname_search:

    filtered_alerts = filtered_alerts[
        filtered_alerts["hostname"]
        .str.contains(
            hostname_search,
            case=False,
            na=False,
        )
    ]

# ---------------------------------------------------
# Header
# ---------------------------------------------------

show_header()

# ---------------------------------------------------
# KPI Metrics
# ---------------------------------------------------

show_metrics(filtered_alerts, exceptions)

st.divider()

# ---------------------------------------------------
# Dashboard Charts
# ---------------------------------------------------

left, right = st.columns(2)

with left:

    st.plotly_chart(
        alerts_by_severity(filtered_alerts),
        use_container_width=True,
    )

with right:

    st.plotly_chart(
        alerts_by_mitre(filtered_alerts),
        use_container_width=True,
    )

st.divider()

# ---------------------------------------------------
# Recent AI Assessments
# ---------------------------------------------------

st.subheader("Recent AI Assessments")

st.info(
    "Assessment history will be connected to "
    "logs/ai_audit.json in the next phase."
)

st.divider()

# ---------------------------------------------------
# Recent Alerts
# ---------------------------------------------------

st.write(
    f"Showing {len(filtered_alerts):,} "
    f"of {len(alerts):,} alerts."
)

st.subheader("Recent Alerts")

columns = [
    "alert_id",
    "timestamp",
    "severity",
    "alert_type",
    "hostname",
    "employee_id",
    "mitre_attack",
]

existing_columns = [
    column
    for column in columns
    if column in alerts.columns
]

st.dataframe(
    filtered_alerts[existing_columns].head(20),
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.caption(
    "Compliance AI • Phase 6 Dashboard • "
    "Cybersecurity Compliance & AI Demonstration"
)