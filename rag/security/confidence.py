"""
Confidence scoring for AI compliance assessments.
"""


def calculate_confidence(
    evidence_count,
    source_count
):

    score = 0


    if evidence_count > 0:
        score += 40


    if evidence_count >= 10:
        score += 30


    if source_count >= 2:
        score += 30


    if score >= 80:

        return "HIGH"


    elif score >= 50:

        return "MEDIUM"


    else:

        return "LOW"