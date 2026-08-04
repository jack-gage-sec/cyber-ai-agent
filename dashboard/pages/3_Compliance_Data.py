import os
import sys

from pathlib import Path

dir_above_cep = Path(__file__).resolve().parents[3]
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), dir_above_cep))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

import streamlit as st

from database.query import (
    get_access_reviews,
    get_policy_exceptions,
)

st.title("Compliance Evidence")

reviews = get_access_reviews()

exceptions = get_policy_exceptions()

st.subheader("Access Reviews")

st.dataframe(reviews)

st.subheader("Policy Exceptions")

st.dataframe(exceptions)
