import streamlit as st
import pandas as pd

from database.query import get_audit_logs


st.title("📝 AI Audit Log")

st.caption(
    "Review AI usage, compliance activity, and system access history."
)


logs = get_audit_logs()


if logs:

    audit_data = []

    for log in logs:
        audit_data.append(
            {
                "Audit ID": log.audit_id,
                "User": log.user,
                "Action": log.action,
                "Table Accessed": log.table_accessed,
                "Record Count": log.record_count,
                "Timestamp": log.timestamp,
                "Purpose": log.purpose,
            }
        )

    df = pd.DataFrame(audit_data)

    st.dataframe(
        df,
        use_container_width=True,
    )

else:

    st.info("No audit events found.")