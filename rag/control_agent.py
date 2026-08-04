"""
AI Control Testing Agent.

Evaluates compliance controls using:
- Policy documents
- Database evidence
- LLM reasoning
"""

import os
import sys

from pathlib import Path

dir_above_cep = Path(__file__).resolve().parents[2]
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), dir_above_cep))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)



from langchain_openai import ChatOpenAI

from rag.retriever import ComplianceRetriever
from rag.prompts import (
    CONTROL_TEST_PROMPT,
    contains_prompt_injection,
)

from database.query import (
    get_control,
    get_access_reviews,
    get_policy_exceptions,
)


class ControlTestingAgent:


    def __init__(self):

        self.retriever = ComplianceRetriever()

        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0,
        )


    def test_control(
        self,
        control_id,
    ):


        # ------------------------------
        # Retrieve policy
        # ------------------------------

        policy_docs = self.retriever.search(
            control_id,
            k=5,
        )


        policy_context = "\n\n".join(
            [
                doc.page_content
                for doc in policy_docs
            ]
        )


        # ------------------------------
        # Gather evidence
        # ------------------------------

        evidence = []


        evidence_context = str(
            evidence[:50]
        )  


        control = get_control(
    	    control_id
	    )


        if not control:
    	    return {
       	        "error":
        	    "Unknown control ID"
    	    }


        # ------------------------------
        # Build prompt
        # ------------------------------

        prompt = CONTROL_TEST_PROMPT.format(
            control_id=control_id,
            policy=policy_context,
            evidence=evidence_context,
        )


        response = self.llm.invoke(
            prompt
        )


        return {
            "control_id": control_id,
            "assessment": response.content,
            "evidence_count": len(evidence),
        }



if __name__ == "__main__":


    agent = ControlTestingAgent()


    while True:

        control = input(
            "\nEnter control ID "
            "(or exit): "
        )


        if control.lower() == "exit":
            break


        result = agent.test_control(
            control
        )


        print("\n====================")
        print("CONTROL ASSESSMENT")
        print("====================")

        print(
            result["assessment"]
        )


        print()

        print(
            "Evidence records reviewed:",
            result["evidence_count"]
        )
