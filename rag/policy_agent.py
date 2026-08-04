"""
Policy Question Answering Agent.

Uses RAG to answer questions against
the compliance policy knowledge base.
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
    POLICY_QA_PROMPT,
    contains_prompt_injection,
)


class PolicyAgent:

    def __init__(self):

        self.retriever = ComplianceRetriever()

        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0,
        )


    def ask(self, question):

        # ------------------------------
        # Prompt injection protection
        # ------------------------------

        if contains_prompt_injection(question):

            return {
                "answer": (
                    "Request blocked because it "
                    "contains a potential prompt "
                    "injection attempt."
                ),
                "sources": [],
            }


        # ------------------------------
        # Retrieve documents
        # ------------------------------

        documents = self.retriever.search(
            question,
            k=5,
        )


        if not documents:

            return {
                "answer": (
                    "No relevant policy evidence "
                    "was found."
                ),
                "sources": [],
            }


        context = "\n\n".join(
            [
                doc.page_content
                for doc in documents
            ]
        )


        # ------------------------------
        # Generate answer
        # ------------------------------

        prompt = POLICY_QA_PROMPT.format(
            context=context,
            question=question,
        )


        response = self.llm.invoke(prompt)


        sources = []

        for doc in documents:

            sources.append(
                {
                    "policy_id":
                        doc.metadata.get(
                            "policy_id"
                        ),

                    "filename":
                        doc.metadata.get(
                            "filename"
                        ),
                }
            )


        return {
            "answer": response.content,
            "sources": sources,
        }



if __name__ == "__main__":

    agent = PolicyAgent()

    while True:

        question = input(
            "\nAsk a policy question "
            "(or type exit): "
        )

        if question.lower() == "exit":
            break


        result = agent.ask(question)


        print("\nAnswer:")
        print(result["answer"])


        print("\nSources:")

        for source in result["sources"]:
            print(source)
