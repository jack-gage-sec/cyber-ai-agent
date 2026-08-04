from datetime import datetime
from pathlib import Path

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

from reportlab.lib.styles import getSampleStyleSheet



REPORT_DIR = Path(
    "reports"
)


def generate_report(
    metrics,
    filename=None,
):

    REPORT_DIR.mkdir(
        exist_ok=True
    )


    if filename is None:

        filename = (
            f"Compliance_Report_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            ".pdf"
        )


    filepath = REPORT_DIR / filename


    document = SimpleDocTemplate(
        str(filepath)
    )


    styles = getSampleStyleSheet()


    content = []


    content.append(
        Paragraph(
            "Compliance AI Report",
            styles["Title"],
        )
    )


    content.append(
        Spacer(1, 12)
    )


    content.append(
        Paragraph(
            f"""
            Generated:
            {datetime.now()}
            """,
            styles["Normal"],
        )
    )


    content.append(
        Spacer(1, 12)
    )


    content.append(
        Paragraph(
            "Executive Summary",
            styles["Heading2"],
        )
    )


    content.append(
        Paragraph(
            f"""
            Total Alerts:
            {metrics['alerts']}
            <br/>
            Critical Alerts:
            {metrics['critical']}
            <br/>
            Policy Exceptions:
            {metrics['exceptions']}
            """,
            styles["Normal"],
        )
    )


    document.build(
        content
    )


    return filepath