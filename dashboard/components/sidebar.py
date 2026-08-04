import streamlit as st


def show_sidebar():

    with st.sidebar:

        st.header("Navigation")

        st.success("System Status")

        st.write("✅ PostgreSQL")

        st.write("✅ ChromaDB")

        st.write("✅ LLM")

        st.divider()

        st.caption("Compliance AI v1.0")