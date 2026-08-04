import pandas as pd
import plotly.express as px


def alerts_by_severity(df):

    counts = (
        df["severity"]
        .value_counts()
        .reset_index()
    )

    counts.columns = [
        "Severity",
        "Count",
    ]

    fig = px.bar(
        counts,
        x="Severity",
        y="Count",
        title="Alerts by Severity",
    )

    return fig



def alerts_by_mitre(df):

    counts = (
        df["mitre_attack"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    counts.columns = [
        "MITRE Technique",
        "Count",
    ]

    fig = px.bar(
        counts,
        x="MITRE Technique",
        y="Count",
        title="Top MITRE ATT&CK Techniques",
    )

    return fig