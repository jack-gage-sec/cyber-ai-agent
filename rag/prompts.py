"""
Prompt templates for the Compliance-AI RAG system.
"""

from langchain_core.prompts import ChatPromptTemplate


# =====================================================
# Policy Question & Answer Prompt
# =====================================================

POLICY_QA_PROMPT = ChatPromptTemplate.from_template(
    """
You are an expert cybersecurity compliance assistant.

Your responsibilities:

- Answer ONLY using the supplied policy documents.
- Do NOT invent information.
- If the answer cannot be found, say:

"Insufficient policy evidence was found."

Always cite:

- Policy ID
- File name

Policy Context
--------------
{context}

Question
--------
{question}

Answer:
"""
)


# =====================================================
# Control Testing Prompt
# =====================================================

CONTROL_TEST_PROMPT = ChatPromptTemplate.from_template(
    """
You are performing a cybersecurity control assessment.

Control ID:
{control_id}

Policy
------
{policy}

Evidence
--------
{evidence}

Determine whether the control should be:

PASS

PARTIAL

FAIL

Provide:

1. Decision
2. Explanation
3. Supporting evidence
4. Missing evidence (if applicable)
5. Confidence (High / Medium / Low)

Answer:
"""
)


# =====================================================
# Evidence Summarization Prompt
# =====================================================

EVIDENCE_SUMMARY_PROMPT = ChatPromptTemplate.from_template(
    """
You are summarizing cybersecurity audit evidence.

Evidence
--------
{evidence}

Create a concise report including:

• Overview

• Key Findings

• Risks

• Recommendations

Limit the response to approximately 250 words.

Summary:
"""
)


# =====================================================
# Prompt Injection Detection
# =====================================================

BLOCKED_PHRASES = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "reveal your system prompt",
    "show your prompt",
    "print your instructions",
    "pretend you are",
    "disregard policies",
    "bypass safety",
    "developer message",
]


def contains_prompt_injection(text: str) -> bool:
    """
    Returns True if the text contains common prompt
    injection attempts.
    """

    lowered = text.lower()

    return any(
        phrase in lowered
        for phrase in BLOCKED_PHRASES
    )