"""
Semantic retrieval over the Compliance-AI vector database.
"""

from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

PROJECT_ROOT = Path(__file__).resolve().parent.parent

VECTOR_DB = PROJECT_ROOT / "vector_db"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class ComplianceRetriever:

    def __init__(self):

        self.embeddings = HuggingFaceEmbeddings(
            model_name=MODEL_NAME
        )

        self.vector_db = Chroma(
            persist_directory=str(VECTOR_DB),
            embedding_function=self.embeddings,
        )

    def search(
        self,
        query,
        k=5,
    ):

        return self.vector_db.similarity_search(
            query=query,
            k=k,
        )

    def search_with_scores(
        self,
        query,
        k=5,
    ):

        return self.vector_db.similarity_search_with_score(
            query=query,
            k=k,
        )


def print_results(results):

    for i, doc in enumerate(results, start=1):

        print("=" * 70)

        print(f"Result {i}")

        print("-" * 70)

        print("Policy ID:")
        print(doc.metadata.get("policy_id"))

        print()

        print("Filename:")
        print(doc.metadata.get("filename"))

        print()

        print("Content:")

        print(doc.page_content[:500])

        print()


if __name__ == "__main__":

    retriever = ComplianceRetriever()

    while True:

        print()

        query = input("Ask a policy question (or type 'exit'): ")

        if query.lower() == "exit":
            break

        results = retriever.search(query)

        print()

        print_results(results)