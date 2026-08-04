import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "D:\Backup Files\Experiments\Compliance Evidence Pipeline"))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

import streamlit as st

from rag.control_agent import ControlTestingAgent

st.title("AI Control Testing")

control = st.text_input(
    "Control ID",
    value="AC-001"
)

if st.button("Run Assessment"):

    agent = ControlTestingAgent()

    result = agent.test_control(control)

    if "error" in result:

        st.error(result["error"])

    else:

        st.subheader("Assessment")

        st.write(result["assessment"])

        st.metric(
            "Confidence",
            result["confidence"]
        )

        st.metric(
            "Evidence Records",
            result["evidence_count"]
        )