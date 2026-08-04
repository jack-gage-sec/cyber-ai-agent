import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "D:\Backup Files\Experiments\Compliance Evidence Pipeline"))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

from rag.prompts import POLICY_QA_PROMPT

prompt = POLICY_QA_PROMPT.format(
    context="Policy ID: AC-001\nQuarterly access reviews are required.",
    question="How often are access reviews performed?"
)

print(prompt)