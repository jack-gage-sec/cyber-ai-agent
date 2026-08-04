def require_role(
    allowed_roles
):

    import streamlit as st


    user_role = (
        st.session_state
        .user["role"]
    )


    if user_role not in allowed_roles:

        st.error(
            "You do not have permission "
            "to access this page."
        )

        st.stop()