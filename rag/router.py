"""
AI Router

Determines which compliance AI agent
should process a user request.
"""

from rag.policy_agent import PolicyAgent
from rag.control_agent import ControlTestingAgent


class AIRouter:


    def __init__(self):

        self.policy_agent = PolicyAgent()

        self.control_agent = ControlTestingAgent()



    def detect_request_type(
        self,
        prompt
    ):

        """
        Determine which AI agent should handle
        the request.
        """

        if not prompt:

            return "error"


        prompt = prompt.strip()


        # Control IDs
        # Example:
        # AC-001
        # AC-002

        if (
            prompt.upper().startswith("AC-")
            and len(prompt) >= 6
        ):

            return "control"


        # Future expansion:
        #
        # "show me alerts"
        # -> alert agent
        #
        # "analyze risk"
        # -> risk agent


        return "policy"



    def run(
        self,
        prompt
    ):

        """
        Route request to the correct AI agent.
        """


        request_type = self.detect_request_type(
            prompt
        )


        if request_type == "error":

            return {

                "status": "error",

                "error":
                    "No prompt provided.",

            }



        if request_type == "control":

            result = (
                self.control_agent.test_control(
                    prompt.strip()
                )
            )


            return self.normalize_response(
                result,
                "control",
            )



        else:

            result = (
                self.policy_agent.ask(
                    prompt.strip()
                )
            )


            return self.normalize_response(
                result,
                "policy",
            )



    def normalize_response(
        self,
        response,
        response_type,
    ):

        """
        Ensure all agents return a consistent format.
        """


        if "error" in response:

            return {

                "status":
                    "error",

                "type":
                    response_type,

                "error":
                    response["error"],

            }


        return {

            "status":
                "success",

            "type":
                response_type,

            "answer":
                response.get(
                    "answer",
                    response.get(
                        "assessment",
                        "",
                    ),
                ),

            "confidence":
                response.get(
                    "confidence",
                    "MEDIUM",
                ),

            "sources":
                response.get(
                    "sources",
                    [],
                ),

            "metadata":
                {

                    "agent":
                        response_type,

                }

        }