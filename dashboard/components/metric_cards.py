import os
import sys

from pathlib import Path

dir_above_cep = Path(__file__).resolve().parents[3]
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), dir_above_cep))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

import streamlit as st


def show_metrics(alerts, exceptions):

    total_alerts = len(alerts)

    critical_alerts = len(
        alerts[
            alerts["severity"] == "Critical"
        ]
    )

    total_exceptions = len(exceptions)

    compliance_score = max(
        0,
        100 - critical_alerts // 5,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Total Alerts",
            f"{total_alerts:,}",
        )

    with c2:
        st.metric(
            "Critical Alerts",
            f"{critical_alerts:,}",
        )

    with c3:
        st.metric(
            "Policy Exceptions",
            f"{total_exceptions:,}",
        )

    with c4:
        st.metric(
            "Compliance Score",
            f"{compliance_score}%",
        )
