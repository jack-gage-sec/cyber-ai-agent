# Compliance AI Platform

An AI-powered cybersecurity and compliance analysis platform that combines Retrieval-Augmented Generation (RAG), compliance evidence management, security analytics, and automated control assessments to help organizations evaluate security posture and audit readiness.

The platform uses organizational policies, compliance evidence, security events, and AI-driven analysis to provide evidence-based answers and automate portions of the compliance review process.

---

# Features

## AI Workspace

An AI assistant that answers cybersecurity and compliance questions using organization-specific policy knowledge.

Capabilities:

- Policy-based question answering
- Retrieval-Augmented Generation (RAG)
- Evidence-grounded responses
- Source document retrieval
- AI confidence scoring

Example questions:

- "What are the requirements for privileged access?"
- "Do current access reviews satisfy least privilege requirements?"
- "What risks exist from current policy exceptions?"

---

## Policy QA

Provides natural language access to organizational policies.

The system processes policy documents and creates a searchable AI knowledge base.

Supported documents include:

- Access Control Policies
- Password Policies
- Incident Response Procedures
- Data Classification Policies
- Security Standards

---

## Evidence Explorer

Provides a centralized location for exploring compliance artifacts.

Evidence sources include:

- Access reviews
- Policy exceptions
- Security alerts
- Audit records
- Control assessments

The Evidence Explorer helps users trace compliance requirements back to supporting evidence.

---

## Compliance Evidence Management

Tracks structured compliance evidence stored in PostgreSQL.

Examples:

- User access reviews
- Approved policy exceptions
- Evidence metadata
- Data classification information

---

## AI Control Testing

Uses AI to evaluate whether security controls are supported by available evidence.

Example:

Control:
