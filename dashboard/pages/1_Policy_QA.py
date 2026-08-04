import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "D:\Backup Files\Experiments\Compliance Evidence Pipeline"))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

import streamlit as st

from rag.policy_agent import PolicyAgent

st.title("Policy Question Answering")

question = st.text_input(
    "Ask a compliance question"
)

if st.button("Ask"):

    if question:

        agent = PolicyAgent()

        result = agent.ask(question)

        st.subheader("Answer")

        st.write(result["answer"])

        st.subheader("Sources")

        for source in result["sources"]:

            st.json(source)