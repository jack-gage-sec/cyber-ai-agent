"""
AI Control Testing Agent.

Evaluates cybersecurity compliance controls using:

- Control mappings from PostgreSQL
- Policy documents from RAG
- Compliance evidence from PostgreSQL
- LLM reasoning
- AI security controls
"""

import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "D:\Backup Files\Experiments\Compliance Evidence Pipeline"))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

from langchain_openai import ChatOpenAI

from rag.retriever import ComplianceRetriever

from rag.prompts import CONTROL_TEST_PROMPT

from database.query import (
    get_control,
    get_access_reviews,
    get_policy_exceptions,
)

from security.input_guard import check_input
from security.output_guard import validate_output
from security.confidence import calculate_confidence
from security.audit_logger import log_event



class ControlTestingAgent:


    def __init__(self):

        self.retriever = ComplianceRetriever()

        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0,
        )


    def collect_evidence(
        self,
        evidence_sources
    ):

        """
        Collect evidence dynamically
        based on control mapping.
        """

        evidence = []


        sources = [
            source.strip()
            for source in evidence_sources.split(",")
        ]


        for source in sources:


            if source == "access_reviews":

                evidence.extend(
                    get_access_reviews()
                )


            elif source == "policy_exceptions":

                evidence.extend(
                    get_policy_exceptions()
                )


            # Additional sources can be
            # added here later:
            #
            # elif source == "alerts":
            #     evidence.extend(
            #         get_alerts()
            #     )


        return evidence



    def test_control(
        self,
        control_id
    ):


        # ---------------------------------
        # Step 1: Input security validation
        # ---------------------------------

        input_check = check_input(
            control_id
        )


        if not input_check["allowed"]:

            return {
                "error":
                    input_check["reason"]
            }



        # ---------------------------------
        # Step 2: Retrieve control mapping
        # ---------------------------------

        control = get_control(
            control_id
        )


        if not control:

            return {
                "error":
                    f"Control {control_id} was not found."
            }



        # ---------------------------------
        # Step 3: Retrieve policy context
        # ---------------------------------

        policy_documents = (
            self.retriever.search(
                control["policy_id"],
                k=5,
            )
        )


        policy_context = "\n\n".join(
            [
                doc.page_content
                for doc in policy_documents
            ]
        )



        # ---------------------------------
        # Step 4: Collect evidence
        # ---------------------------------

        evidence = self.collect_evidence(
            control["evidence_sources"]
        )


        evidence_context = str(
            evidence[:50]
        )



        # ---------------------------------
        # Step 5: Create LLM prompt
        # ---------------------------------

        prompt = CONTROL_TEST_PROMPT.format(

            control_id=control_id,

            policy=policy_context,

            evidence=evidence_context,

        )



        # ---------------------------------
        # Step 6: Generate assessment
        # ---------------------------------

        response = self.llm.invoke(
            prompt
        )



        # ---------------------------------
        # Step 7: Validate AI output
        # ---------------------------------

        validation = validate_output(
            response.content
        )



        # ---------------------------------
        # Step 8: Calculate confidence
        # ---------------------------------

        confidence = calculate_confidence(

            evidence_count=len(evidence),

            source_count=len(policy_documents)

        )



        # ---------------------------------
        # Step 9: Log AI decision
        # ---------------------------------

        log_event(

            user_input=control_id,

            response=response.content,

            metadata={

                "control_id":
                    control_id,

                "policy_id":
                    control["policy_id"],

                "evidence_sources":
                    control["evidence_sources"],

                "evidence_count":
                    len(evidence),

                "confidence":
                    confidence,

                "output_validation":
                    validation,

            }

        )



        return {

            "control_id":
                control_id,

            "assessment":
                response.content,

            "confidence":
                confidence,

            "evidence_count":
                len(evidence),

            "validation":
                validation,

        }




if __name__ == "__main__":

    security_check = check_input(control_id)

    if not security_check["allowed"]:

        return {
            "error":
            security_check["reason"]
        }

    agent = ControlTestingAgent()


    while True:


        control = input(
            "\nEnter Control ID "
            "(or type exit): "
        )


        if control.lower() == "exit":

            break



        result = agent.test_control(
            control
        )


        print("\n==============================")
        print("CONTROL ASSESSMENT")
        print("==============================\n")


        if "error" in result:

            print(result["error"])

            continue


        print(
            result["assessment"]
        )


        print("\n------------------------------")

        print(
            "Confidence:",
            result["confidence"]
        )

        print(
            "Evidence Records:",
            result["evidence_count"]
        )

        print(
            "Validation:",
            result["validation"]
        )

        validation = validate_output(
            response.content
        )


        confidence = calculate_confidence(
            len(evidence),
            len(policy_docs)
        )


        log_event(

            user_input=control_id,

            response=response.content,

            metadata={

                "validation":
                    validation,

                "confidence":
                    confidence,

                "evidence_count":
                    len(evidence)

            }

        )