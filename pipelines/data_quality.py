"""
Data quality checks for compliance pipeline.
"""


def check_duplicate_ids(df, id_column):

    duplicates = (
        df[id_column]
        .duplicated()
        .sum()
    )

    if duplicates > 0:
        raise ValueError(
            f"{duplicates} duplicate IDs found in {id_column}"
        )

    return True



def check_required_values(df, columns):

    missing = (
        df[columns]
        .isnull()
        .sum()
    )

    failures = missing[missing > 0]

    if len(failures) > 0:
        raise ValueError(
            f"Missing values:\n{failures}"
        )

    return True



def check_record_count(df, minimum=1):

    if len(df) < minimum:
        raise ValueError(
            "Dataset contains too few records"
        )

    return True