import json

from pathlib import Path

import pandas as pd


AUDIT_FILE = Path(
    "logs/ai_audit.json"
)


def load_audit_history():

    if not AUDIT_FILE.exists():

        return pd.DataFrame()


    records = []


    with open(
        AUDIT_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:

            records.append(
                json.loads(line)
            )


    return pd.DataFrame(records)