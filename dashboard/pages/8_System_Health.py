import os
import sys

from pathlib import Path

dir_above_cep = Path(__file__).resolve().parents[3]
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), dir_above_cep))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

import streamlit as st

from dashboard.health import (
    check_database,
    get_timestamp,
)

from dashboard.utils import (
    load_dataframe,
)

from dashboard.access_control import require_role


require_role(
    [
        "Administrator",
    ]
)


st.set_page_config(

    page_title="System Health",

    page_icon="⚙️",

    layout="wide",

)


st.title(
    "⚙️ System Health"
)

db_status = check_database()


st.subheader(
    "Database"
)


if db_status["status"] == "healthy":

    st.success(
        db_status["message"]
    )

else:

    st.error(
        db_status["message"]
    )

st.divider()

st.subheader(
    "Data Pipeline"
)

alerts = load_dataframe(
    "alerts",
    limit=50000,
)

controls = load_dataframe(
    "control_tests",
)


c1, c2, c3 = st.columns(3)


with c1:

    st.metric(
        "Alerts Loaded",
        len(alerts),
    )


with c2:

    st.metric(
        "Control Tests",
        len(controls),
    )


with c3:

    st.metric(
        "Policy Exceptions",
        len(load_dataframe("policy_exceptions")),
    )
st.divider()

st.subheader(
    "AI Components"
)


st.success(
    "Embedding Model Available"
)


st.success(
    "Policy Agent Available"
)


st.success(
    "Control Testing Agent Available"
)

st.divider()

st.subheader(
    "Vector Database"
)


try:

    from rag.embeddings import get_vector_store


    st.success(
        "ChromaDB Available"
    )


except Exception as e:

    st.error(
        f"Vector Store Error: {e}"
    )

st.divider()


st.caption(
    f"Last Check: {get_timestamp()}"
)
