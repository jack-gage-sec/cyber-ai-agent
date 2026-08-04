import os
import sys

from pathlib import Path

dir_above_cep = Path(__file__).resolve().parents[3]
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), dir_above_cep))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

import streamlit as st
import pandas as pd

from database.query import get_control_tests


st.title("Control Assessment History")

tests = get_control_tests()


if tests:

    data = []

    for test in tests:
        data.append(
            {
                "Test ID": test.test_id,
                "Control ID": test.control_id,
                "Framework": test.framework,
                "Result": test.result,
                "Evidence ID": test.evidence_id,
                "Tester": test.tester,
                "Test Date": test.test_date,
                "Finding": test.finding,
            }
        )

    st.dataframe(
        pd.DataFrame(data),
        use_container_width=True
    )

else:
    st.info("No assessments found.")
