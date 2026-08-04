import pandas as pd
import numpy as np

from faker import Faker

from constants import (
    FRAMEWORKS,
    CONTROL_IDS,
    TESTERS,
    FINDINGS,
)

fake = Faker()


CONTROL_DESCRIPTIONS = {

    "AC-01":
        "Access control policy is documented and maintained.",

    "AC-02":
        "User access is reviewed periodically and unauthorized access is removed.",

    "AC-03":
        "Access enforcement mechanisms restrict unauthorized access.",

    "CM-01":
        "Configuration management policies are established.",

    "CM-02":
        "Systems maintain approved baseline configurations.",

    "CM-03":
        "Configuration changes are controlled and documented.",

    "IA-01":
        "Identification and authentication policies are maintained.",

    "IA-02":
        "Users are uniquely identified and authenticated.",

    "IR-01":
        "Incident response policies are established.",

    "IR-02":
        "Incident response procedures are tested."
}


def determine_failure_probability(
        control_id,
        access_reviews=None,
        policy_exceptions=None):


    probability = 0.15


    if control_id.startswith("AC"):

        if access_reviews is not None:

            failed_reviews = (
                access_reviews["approved"] == False
            ).sum()

            if failed_reviews > 0:
                probability += 0.20


    if policy_exceptions is not None:

        high_risk = (
            policy_exceptions["risk_level"] == "High"
        ).sum()

        if high_risk > 0:
            probability += 0.10


    return min(probability, 0.75)



def generate_control_tests(
        number,
        access_reviews=None,
        policy_exceptions=None):


    tests = []


    for i in range(number):

        control_id = np.random.choice(
            CONTROL_IDS
        )


        failure_probability = determine_failure_probability(
            control_id,
            access_reviews,
            policy_exceptions
        )


        result = np.random.choice(
            ["FAIL", "PASS"],
            p=[
                failure_probability,
                1 - failure_probability
            ]
        )


        if result == "FAIL":

            finding = np.random.choice(
                FINDINGS[:-1]
            )

        else:

            finding = (
                "Control operating effectively."
            )


        test = {

            "test_id":
                f"TEST{i:06d}",

            "control_id":
                control_id,

            "control_description":
                CONTROL_DESCRIPTIONS[control_id],

            "framework":
                np.random.choice(
                    FRAMEWORKS
                ),

            "result":
                result,

            "evidence_id":
                f"EV{i:06d}",

            "tester":
                np.random.choice(
                    TESTERS
                ),

            "test_date":
                fake.date_between(
                    start_date="-180d",
                    end_date="today"
                ),

            "finding":
                finding

        }


        tests.append(test)


    return pd.DataFrame(tests)