"""
Document loader for Compliance-AI.

Loads every policy document from the policies directory
and converts it into LangChain Document objects.
"""

from pathlib import Path

from langchain_core.documents import Document

PROJECT_ROOT = Path(__file__).resolve().parent.parent

POLICY_DIR = PROJECT_ROOT / "policies"


def load_documents():
    """
    Load every .txt policy document.

    Returns
    -------
    list[Document]
    """

    documents = []

    if not POLICY_DIR.exists():
        raise FileNotFoundError(
            f"Policy directory not found:\n{POLICY_DIR}"
        )

    for file in sorted(POLICY_DIR.glob("*.txt")):

        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        # Try to identify the policy ID
        policy_id = "UNKNOWN"

        for line in text.splitlines():

            if line.startswith("Policy ID"):

                policy_id = line.split(":")[1].strip()
                break

        document = Document(
            page_content=text,
            metadata={
                "filename": file.name,
                "policy_id": policy_id,
                "path": str(file),
            },
        )

        documents.append(document)

    return documents


if __name__ == "__main__":

    docs = load_documents()

    print(f"\nLoaded {len(docs)} documents.\n")

    for doc in docs:

        print("=" * 60)

        print(doc.metadata)

        print()

        print(doc.page_content[:250])

        print()