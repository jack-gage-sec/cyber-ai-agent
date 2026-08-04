"""
Input security checks for AI requests.
"""


BLOCKED_PATTERNS = [

    "ignore previous instructions",

    "ignore all previous instructions",

    "reveal your system prompt",

    "show me your instructions",

    "developer message",

    "bypass security",

    "disable safeguards",

    "pretend you are",

]


def check_input(text):

    """
    Detect possible prompt injection attempts.

    Returns:
        {
            "allowed": True/False,
            "reason": message
        }
    """

    text_lower = text.lower()


    for pattern in BLOCKED_PATTERNS:

        if pattern in text_lower:

            return {
                "allowed": False,
                "reason":
                    f"Blocked phrase detected: {pattern}"
            }


    return {
        "allowed": True,
        "reason": "Input accepted"
    }