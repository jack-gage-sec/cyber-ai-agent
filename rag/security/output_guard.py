"""
Output validation for AI responses.
"""


REQUIRED_TERMS = [

    "evidence",

    "policy",

]


def validate_output(response):

    """
    Basic validation of AI-generated output.
    """

    response_lower = response.lower()


    missing = []


    for term in REQUIRED_TERMS:

        if term not in response_lower:

            missing.append(term)


    if missing:

        return {
            "valid": False,
            "missing": missing
        }


    return {
        "valid": True,
        "missing": []
    }