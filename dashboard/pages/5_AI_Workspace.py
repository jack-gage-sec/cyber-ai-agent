import os
import sys

from pathlib import Path

dir_above_cep = Path(__file__).resolve().parents[3]
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), dir_above_cep))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

import streamlit as st

from rag.router import AIRouter

from dashboard.access_control import require_role


require_role(
    [
        "Administrator",
        "Analyst",
        "Auditor",
    ]
)


st.set_page_config(
    page_title="AI Workspace",
    page_icon="🤖",
)


st.title("🤖 Compliance AI Assistant")

st.caption(
    "Ask policy questions or run compliance assessments."
)


# ---------------------------------------------------
# Initialize Session State
# ---------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


if "router" not in st.session_state:

    st.session_state.router = AIRouter()



# ---------------------------------------------------
# Display Previous Messages
# ---------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )



# ---------------------------------------------------
# User Input
# ---------------------------------------------------

prompt = st.chat_input(
    "Ask about compliance..."
)



if prompt:


    # Store user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )


    with st.chat_message("user"):

        st.markdown(prompt)



    # ------------------------------------------------
    # Run AI Router
    # ------------------------------------------------

    response = st.session_state.router.run(
        prompt
    )



    # ------------------------------------------------
    # Display AI Response
    # ------------------------------------------------

    with st.chat_message("assistant"):


        if response["status"] == "success":


            st.markdown(
                response["answer"]
            )


            if response.get("confidence"):

                st.metric(
                    "Confidence",
                    response["confidence"],
                )



            if response.get("sources"):


                with st.expander(
                    "Sources"
                ):

                    for source in response["sources"]:

                        st.write(source)



        else:


            st.error(
                response["error"]
            )



    # ------------------------------------------------
    # Save Assistant Response
    # ------------------------------------------------

    assistant_message = response.get(
        "answer",
        response.get(
            "error",
            "",
        ),
    )


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_message,
        }
    )
