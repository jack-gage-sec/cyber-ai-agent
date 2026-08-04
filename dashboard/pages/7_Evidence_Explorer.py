import os
import sys

from pathlib import Path

dir_above_cep = Path(__file__).resolve().parents[3]
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), dir_above_cep))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

import streamlit as st
import pandas as pd

from dashboard.utils import load_dataframe

st.set_page_config(
    page_title="Evidence Explorer",
    page_icon="🔎",
    layout="wide",
)

st.title(
    "🔎 Compliance Evidence Explorer"
)

evidence_type = st.selectbox(

    "Evidence Type",

    [
        "alerts",
        "access_reviews",
        "policy_exceptions",
        "control_tests",
    ]

)

data = load_dataframe(
    evidence_type,
    limit=5000,
)

search_term = st.text_input(
    "Search evidence"
)


filtered = data.copy()


if search_term:

    filtered = filtered[
        filtered.astype(str)
        .apply(
            lambda row:
            row.str.contains(
                search_term,
                case=False,
                na=False,
            )
            .any(),
            axis=1,
        )
    ]

st.write(
    f"Showing {len(filtered):,} records"
)

st.dataframe(

    filtered,

    use_container_width=True,

    hide_index=True,

)

st.divider()

st.subheader(
    "Record Details"
)

if not filtered.empty:

    index = st.number_input(

        "Select row number",

        min_value=0,

        max_value=len(filtered)-1,

        value=0,

    )


    selected = filtered.iloc[index]


    st.json(
        selected.to_dict()
    )

csv = filtered.to_csv(
    index=False
)


st.download_button(

    "Download Evidence CSV",

    csv,

    file_name=f"{evidence_type}.csv",

    mime="text/csv",

)
