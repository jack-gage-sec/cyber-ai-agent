import streamlit as st

from dashboard.report_generator import (
    generate_report,
)

from dashboard.utils import (
    load_dataframe,
)

from dashboard.access_control import require_role


require_role(
    [
        "Administrator",
        "Auditor",
    ]
)



st.title(
    "📄 Compliance Report Generator"
)


alerts = load_dataframe(
    "alerts",
    limit=50000,
)


exceptions = load_dataframe(
    "policy_exceptions",
)



metrics = {

    "alerts":
        len(alerts),

    "critical":
        len(
            alerts[
                alerts["severity"]
                == "Critical"
            ]
        ),

    "exceptions":
        len(exceptions),

}



st.write(
    "Generate an audit-ready compliance report."
)



if st.button(
    "Generate Report"
):

    report = generate_report(
        metrics
    )


    st.success(
        "Report generated."
    )


    with open(
        report,
        "rb",
    ) as file:


        st.download_button(

            "Download PDF",

            file,

            file_name=report.name,

            mime="application/pdf",

        )