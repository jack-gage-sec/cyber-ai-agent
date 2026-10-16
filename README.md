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



## Prompt Injection Research — Red Team / Blue Team Pipeline

An extension of the autonomous red team / blue team pipeline adding
prompt injection testing against a real LLM-backed target application.
This project tests both **direct prompt injection** (payloads submitted
to an LLM application) and **indirect prompt injection** (malicious
instructions embedded in data a defensive agent reads), and measures the
gap between injection success and detection across three security levels.

> **Lab use only.** All targets are intentionally vulnerable applications
> running on isolated VMs you own or have explicit written authorization
> to test. Do not run this against any real, production, or third-party
> system.


---

### What this project adds

The base red team / blue team pipeline tested traditional web
vulnerabilities (SQL injection, XSS, command injection, LFI, brute force)
against DVWA. This branch extends that pipeline with:

- A **real LLM target application** (`vulnerable_llm_target.py`) — a
  Flask/Claude app with three configurable security levels, replacing
  DVWA's XSS surface as the injection target
- **Direct prompt injection testing** across LOW, MEDIUM, and HIGH
  security levels, measuring how much resistance each level provides
- **Indirect prompt injection** planted into DVWA's guestbook to test
  whether the blue team detection agent can be manipulated through data
  it reads
- **Dual-stage injection screening** in the blue team agent to detect
  and resist injection content propagating through the analysis pipeline

---

### Architecture

```
[Attacker VM]                          [Target / Defender VM]

recon_vuln_agent_injection.py
  └── test_llm_target_injection.py
        │
        ├── POST /chat ─────────────> vulnerable_llm_target.py (Flask/Claude)
        │   (direct injection)              └── llm_target_access.log
        │                                           │
        └── POST guestbook ────────> DVWA guestbook (indirect injection)
            (indirect injection)                    │
                                                    ▼
                                        detection_agent_injection.py
                                          ├── read_apache_logs_safe
                                          │   (screens for injection)
                                          ├── analyze_log_for_attacks
                                          │   (prompt injection signatures)
                                          ├── screen_findings_for_injection
                                          │   (final injection check)
                                          └── alert report
```

**Two distinct injection types, two distinct targets:**

| Type | Target | Purpose |
|---|---|---|
| Direct | Flask app `/chat` | Test LLM application resistance to user-supplied injection |
| Indirect | DVWA guestbook | Test blue team agent robustness to injection in data it reads |

---

### Repo structure

```
prompt_injection/
├── recon_vuln_agent_injection.py     # red team pipeline
├── test_llm_target_injection.py      # Flask injection tools (imported by red team)
├── vulnerable_llm_target.py          # deliberately vulnerable Flask/Claude target
└── detection_agent_injection.py      # blue team detection pipeline
```

### Files

| File | VM | Description |
|---|---|---|
| `prompt_injection/recon_vuln_agent_injection.py` | Attacker | Red team pipeline: recon → plan → human approval → exploitation + injection |
| `prompt_injection/test_llm_target_injection.py` | Attacker | LangChain tools for Flask target injection testing (imported by red team agent) |
| `prompt_injection/vulnerable_llm_target.py` | Target | Deliberately vulnerable Flask/Claude app — the real LLM injection target |
| `prompt_injection/detection_agent_injection.py` | Defender | Blue team agent: log analysis with injection screening and prompt injection signatures |

Both files on the attacker VM must be in the same directory —
`recon_vuln_agent_injection.py` imports `test_llm_target_injection.py`
directly, so they need to be co-located when run.

---

### The Flask target — three security levels

`vulnerable_llm_target.py` is a Flask application that passes user input
to Claude via the Anthropic API. It supports three security levels that
can be changed at runtime, allowing the same payloads to be tested under
different resistance conditions:

| Level | Defense | Expected behavior |
|---|---|---|
| **LOW** | None — input passed directly to Claude | Injection attempts reach the LLM unfiltered |
| **MEDIUM** | Regex keyword filter blocks obvious patterns | Common injection phrases blocked; rephrased variants bypass |
| **HIGH** | Explicit injection-resistance instructions in system prompt | LLM instructed to treat user input as untrusted data |

The cross-level comparison — running the same payload set at all three
levels and measuring success rates — is the core research measurement
this project produces.

---

### Key findings

**Direct injection (Flask target):**
- MEDIUM regex filter blocked 40% of payloads; the remaining 60% bypassed
  it by rephrasing (e.g. `act as` instead of `you are now`, indirect
  framing instead of direct commands)
- The filter patterns are keyword-based and bypassable by any attacker
  who can observe which phrases trigger a block
- Security level changes via `/security` were logged and detected by the
  blue team agent as pre-attack defense reduction — an emergent detection
  capability not explicitly programmed

**Indirect injection (DVWA guestbook):**
- Five injection techniques planted in a single payload: instruction
  masquerade, goal redirection, persona override, exfiltration attempt,
  and alert suppression
- The blue team agent read the planted content, flagged it at two
  independent pipeline stages (`read_apache_logs_safe` and
  `screen_findings_for_injection`), and was not influenced by any
  embedded instructions
- Injected directives were treated as data to report, not commands
  to follow

**Detection findings:**
- Dual-stage screening pipeline successfully flagged injection content
  propagating through the analysis chain without producing false
  behavioral influence
- Blue team agent correctly reconstructed the attack timeline from log
  data alone, including identifying automated behavior from request
  timing and inferring pre/post-attack security manipulation from the
  sequence of `/security` changes relative to `/chat` requests

---

### Known limitations

- **Regex signatures miss encoded payloads.** Both the Flask filter and
  the blue team detection signatures match literal strings only — URL
  encoding, Unicode lookalikes, or base64-wrapped payloads bypass all
  signature-based detection entirely
- **Cross-level comparison incomplete.** API connectivity issues during
  testing caused HTTP 500 errors at LOW and HIGH, so clean LLM responses
  were only observed at MEDIUM. Full results require a Flask VM with
  reliable access to `api.anthropic.com`
- **Indirect injection limited to guestbook surface.** The planted
  content only appears in DVWA's stored XSS page. A real adversary could
  embed injection content in any data source the blue team agent reads —
  log files, fetched web pages, API responses, or database query results
- **No semantic injection detection.** The screening pipeline uses the
  same regex patterns as the attack signatures. A semantically equivalent
  injection phrased without trigger keywords would pass all screens
  undetected
- **Flask target has no authentication on `/security`.** Any client can
  change the security level without authorization, which enabled the
  observed pre-attack defense reduction. In a hardened deployment this
  endpoint would require authentication

---

### Ethical and legal notice

This project is for authorized security research in isolated lab
environments only. The tools, payloads, and techniques demonstrated here
are designed for use against intentionally vulnerable software
(DVWA, `vulnerable_llm_target.py`) that you control. Using these tools
against systems you do not own or have explicit written authorization to
test may constitute unauthorized access under applicable computer fraud
laws regardless of intent.
