# Compliance AI Platform

The Compliance AI Platform is an AI-powered cybersecurity and compliance application designed to streamline compliance analysis, evidence management, and policy retrieval. By combining a Large Language Model (LLM), Retrieval-Augmented Generation (RAG), PostgreSQL, SQLAlchemy, and Streamlit, the platform enables users to search organizational policies, analyze compliance evidence, perform AI-assisted control testing, and monitor overall compliance posture through a unified dashboard.

> **Disclaimer:** All policies, users, security events, compliance records, and other data used throughout this project are entirely fictitious and were created solely for demonstration and experimentation purposes. No real organizational or personally identifiable information is included.

---

# Features

## Home Dashboard

The home page provides a high-level overview of the organization's compliance and security posture. It summarizes compliance metrics, recent AI assessments, security alerts, and key findings, giving users a quick snapshot of current risk and compliance status.

---

## Policy QA

Policy QA enables users to ask natural language questions about organizational policies. Using Retrieval-Augmented Generation (RAG), the application retrieves relevant policy information from the knowledge base and generates evidence-grounded responses.

Example questions include:

* What are the requirements for privileged access?
* How often should access reviews be performed?
* What is the organization's password policy?

---

## AI Control Testing

The AI Control Testing page evaluates security and compliance controls against available evidence. Users provide a control identifier, and the platform generates:

* Pass/Fail assessment
* Supporting evidence
* AI-generated recommendation

---

## Compliance Evidence

The Compliance Evidence page displays structured compliance evidence stored within the PostgreSQL database.

Current evidence includes:

* Access Reviews
* Policy Exceptions

These records provide visibility into user access, approved exceptions, reviewers, approval status, and supporting compliance information.

---

## AI Audit Log

The AI Audit Log records system activity to support AI governance and auditability.

Each audit record includes:

* User
* Action performed
* Resource accessed
* Timestamp
* Purpose
* Records processed

---

## AI Workspace

The AI Workspace provides an interactive chatbot capable of answering compliance questions and assisting with compliance-related tasks.

Users can:

* Ask policy questions
* Generate compliance assessments
* Retrieve organizational knowledge
* Explore compliance information using AI

---

## Assessment History

Assessment History maintains a historical record of AI-generated control assessments.

Each assessment includes:

* Control identifier
* Framework
* Assessment result
* Evidence reviewed
* Findings
* Test date

This allows users to review previous compliance evaluations and track assessment outcomes over time.

---

## Evidence Explorer

The Evidence Explorer provides a centralized interface for browsing compliance evidence collected throughout the organization.

Users can review evidence records, investigate supporting documentation, and better understand how evidence supports compliance activities.

---

## System Health

System Health monitors the operational status of the Compliance AI Platform.

Health checks include:

* PostgreSQL database connectivity
* Data pipeline status
* Chroma vector database availability
* AI model availability

This page provides operational visibility into the platform's core services.

