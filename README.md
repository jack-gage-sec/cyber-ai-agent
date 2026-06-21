# ai-redteam-blueteam-lab

Two LLM agents, two VMs, one approval gate. This project pairs an autonomous
**red team agent** (recon + vulnerability testing against a deliberately
vulnerable web app) with an independent **blue team agent** (log-based attack
detection) to explore how agentic AI can assist on both sides of a security
workflow — and where a human needs to stay in the loop.

> **Lab use only.** This project targets [DVWA](https://github.com/digininja/DVWA)
> (Damn Vulnerable Web Application), which is intentionally insecure software
> built for security training. Everything here assumes an isolated lab network
> with no production systems, real credentials, or third-party targets
> involved. Do not point these tools at any system you don't own or have
> explicit authorization to test.

📝 Full writeup with architecture, design rationale, and results: **[blog post link]**

## What's here

| File | Description |
|---|---|
| `recon_vuln_agent.py` | Red team pipeline: recon → plan → human approval → exploitation, targeting DVWA |
| `detection_agent.py` | Blue team agent: reads Apache access logs, flags attack signatures, generates an alert report |

## Architecture, in brief

```
[Attacker VM]                              [Defender VM]
recon agent → plan → human approval? → vuln agent
                                            │
                                            ▼
                                    Apache access.log
                                            │
                                            ▼
                                   detection agent → alert report
```

- **Recon agent** runs read-only reconnaissance (`nmap`, `gobuster`, header
  grabbing) against the target and summarizes findings.
- **Planning step** has the LLM propose which vulnerability classes are worth
  testing and why — without executing anything.
- **Human approval gate** is required before any exploitation traffic is
  sent. If declined, the pipeline stops and only recon + plan are saved.
- **Vulnerability agent** runs DVWA-specific tests (SQL injection, reflected
  XSS, command injection, brute force, local file inclusion) only after
  approval, and produces a findings report.
- **Detection agent**, running independently on a separate VM, reads the
  target's Apache access log, matches attack signatures, attributes activity
  by source IP, and generates a structured alert report — with no shared
  state with the attacking agents beyond the log file itself.

## Why the approval gate

The split between *planning* and *execution* is deliberate. The agent reasons
about what to test and why, but nothing is sent to the target until a human
explicitly approves the plan. This is the core safety property of the
project: autonomy in analysis, a checkpoint before any action with real
effect.

## Requirements

- Two VMs (or isolated network segments): one running DVWA, one for
  detection/log analysis
- Python 3.10+
- `nmap`, `gobuster` installed on the recon VM
- An Anthropic API key (`.env` with `ANTHROPIC_API_KEY=...`)
- `pip install -r requirements.txt` (langchain-anthropic, langgraph,
  langchain-core, requests, python-dotenv)

See the blog post for full setup details, sample output, and discussion of
limitations.

## Known limitations

- Signature-based detection (regex) is brittle against evasion or novel
  payloads — this is a demonstration, not a production IDS
- Brute-force detection uses a flat per-IP request threshold, which can
  false-positive on legitimate traffic
- Detection agent only reads the last 100 lines of the log per run
- IP extraction assumes IPv4 and standard Apache combined log format
- Everything here is scoped to a known-vulnerable lab target (DVWA), not a
  hardened or production environment

## License

[Add your license here]
