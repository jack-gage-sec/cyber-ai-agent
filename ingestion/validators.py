"""
Data validation utilities.
"""


def validate_columns(df, required_columns):
    """
    Ensure required columns exist.
    """

    missing = []

    for column in required_columns:
        if column not in df.columns:
            missing.append(column)

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    return True



def validate_empty_records(df):
    """
    Prevent empty datasets.
    """

    if df.empty:
        raise ValueError(
            "Dataset contains no records"
        )

    return True



def validate_null_values(df):
    """
    Detect missing values.
    """

    nulls = df.isnull().sum()

    invalid = nulls[nulls > 0]

    if len(invalid) > 0:

        raise ValueError(
            f"Null values detected:\n{invalid}"
        )

    return True



def validate_alert_severity(df):

    allowed = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    invalid = df[
        ~df["severity"].isin(allowed)
    ]

    if not invalid.empty:
        raise ValueError(
            "Invalid alert severity detected"
        )

    return True



def validate_control_results(df):

    allowed = [
        "PASS",
        "FAIL"
    ]

    invalid = df[
        ~df["result"].isin(allowed)
    ]

    if not invalid.empty:
        raise ValueError(
            "Invalid control result detected"
        )

    return True