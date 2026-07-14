**Cybersecurity AI Agent Research**

A collection of research projects exploring how AI agents can be applied to
offensive and defensive security workflows — and where the boundaries of
autonomy, safety, and capability interact.

Each project lives in its own branch with full documentation, sample output,
and tests. This README serves as an index.


**Projects

Autonomous Red Team / Blue Team Pipeline**

**Branch:** red-team-blue-team · **Status:** Complete

Two LLM-based agents — one offensive, one defensive — running across two
isolated VMs against a deliberately vulnerable web application. The red team
agent performs reconnaissance and vulnerability exploitation; the blue team
agent independently detects and attributes those actions from Apache access
logs alone, with no shared state between them.

The core research question: where should autonomy stop in an agentic security
pipeline? A human approval checkpoint separates the agent's planning from its
execution — the agent proposes a plan and explains its reasoning, but cannot
act without explicit authorization.

**Key findings:**


The approval gate held up as intended across all test runs — no exploitation
traffic was ever sent without explicit human authorization
The blue team agent correctly detected and attributed all attacks in testing
Just under half of vulnerabilities discovered during reconnaissance could
not be successfully exploited — a gap between discovery and exploitation
that is a central research question for further work
Signature-based detection missed URL-encoded payloads entirely, a real
limitation documented in the test suite


Stack: Python, LangChain, LangGraph, Claude API (Anthropic), DVWA, Apache

📄 Branch README · 🏗️ Architecture deep dive · 📊 Sample output


<!--
To add a new project, copy the block below and fill in the details:

### Project Name
**Branch:** [`branch-name`](#) · **Status:** In Progress / Complete

One paragraph describing the project and the research question it addresses.

**Key findings:**
- Finding 1
- Finding 2

**Stack:** tools, frameworks, models used

📄 [Branch README](#) · 🏗️ [Architecture deep dive](#) · 📊 [Sample output](#)

---
-->
**Research focus**

These projects sit at the intersection of three areas:


**Agentic AI in security contexts** — what can autonomous agents do in
offensive and defensive security workflows, and what can't they do yet?
**The offense/defense boundary** — does AI capability scale symmetrically
to both sides, or does it create asymmetries that favor one over the other?
**Human-in-the-loop design** — where should autonomy stop, and what does
a well-designed approval checkpoint look like in a security-critical system?


**Ethics and scope**


All projects in this repo target intentionally vulnerable, isolated lab
environments (e.g. DVWA) with no production systems, real credentials, or
third-party targets involved. Do not use any of this tooling against systems
you do not own or have explicit authorization to test.



**About**

Cybersecurity engineer with six years of experience, currently researching
the application of large language models and autonomous agents to security
workflows. Interested in the design tradeoffs between agent autonomy and
human oversight in security-critical systems.

📝 Blog: https://www.jackgage.net/blog · 💼 LinkedIn: https://www.linkedin.com/in/jack-gage-5a4b45157/
