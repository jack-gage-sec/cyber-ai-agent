import os
import sys

from pathlib import Path

dir_above_cep = Path(__file__).resolve().parents[2]
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), dir_above_cep))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

from rag.prompts import POLICY_QA_PROMPT

prompt = POLICY_QA_PROMPT.format(
    context="Policy ID: AC-001\nQuarterly access reviews are required.",
    question="How often are access reviews performed?"
)

print(prompt)
