import os


def export_csv(dataframe, filename):

    os.makedirs(
        "synthetic_data/output",
        exist_ok=True
    )

    dataframe.to_csv(
        f"synthetic_data/output/{filename}",
        index=False
    )