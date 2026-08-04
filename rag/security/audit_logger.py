"""
AI activity logging.
"""

import json
from datetime import datetime
from pathlib import Path


LOG_FILE = Path(
    "logs/ai_audit.json"
)


def log_event(
    user_input,
    response,
    metadata=None
):

    LOG_FILE.parent.mkdir(
        exist_ok=True
    )


    event = {

        "timestamp":
            datetime.utcnow().isoformat(),

        "input":
            user_input,

        "response":
            response,

        "metadata":
            metadata or {}

    }


    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(event)
            + "\n"
        )