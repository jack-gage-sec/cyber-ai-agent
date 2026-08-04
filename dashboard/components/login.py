import os
import sys

from pathlib import Path

dir_above_cep = Path(__file__).resolve().parents[3]
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), dir_above_cep))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

import streamlit as st

from security.auth import authenticate



def login():

    st.title(
        "🔐 Compliance AI Login"
    )


    username = st.text_input(
        "Username"
    )


    password = st.text_input(
        "Password",
        type="password",
    )


    if st.button(
        "Login"
    ):

        user = authenticate(
            username,
            password,
        )


        if user:

            st.session_state.user = user

            st.success(
                "Login successful"
            )

            st.rerun()


        else:

            st.error(
                "Invalid credentials"
            )
