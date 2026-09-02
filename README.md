# Prompt Injection Research — Red Team / Blue Team Pipeline

An extension of the [autonomous red team / blue team pipeline](#) adding
prompt injection testing against a real LLM-backed target application.
This project tests both **direct prompt injection** (payloads submitted
to an LLM application) and **indirect prompt injection** (malicious
instructions embedded in data a defensive agent reads), and measures the
gap between injection success and detection across three security levels.

> **Lab use only.** All targets are intentionally vulnerable applications
> running on isolated VMs you own or have explicit written authorization
> to test. Do not run this against any real, production, or third-party
> system.

📝 Full writeup: **[blog post link]** · 🏗️ Architecture deep dive: [`docs/architecture.md`](#)

---

## What this project adds

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

## Architecture

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

## Files

| File | VM | Description |
|---|---|---|
| `recon_vuln_agent_injection.py` | Attacker | Red team pipeline: recon → plan → human approval → exploitation + injection |
| `test_llm_target_injection.py` | Attacker | LangChain tools for Flask target injection testing (imported by red team agent) |
| `vulnerable_llm_target.py` | Target | Deliberately vulnerable Flask/Claude app — the real LLM injection target |
| `detection_agent_injection.py` | Defender | Blue team agent: log analysis with injection screening and prompt injection signatures |

---

## The Flask target — three security levels

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

## Key findings

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

## Known limitations

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

## Requirements

**Attacker VM:**
```
pip install langchain-anthropic langgraph langchain-core requests python-dotenv
```
- `nmap` and `gobuster` installed
- `.env` file with `ANTHROPIC_API_KEY`

**Target / Defender VM:**
```
pip install flask anthropic python-dotenv
```
- DVWA running and accessible
- Outbound access to `api.anthropic.com` on port 443 (required by Flask app)
- `.env` file with `ANTHROPIC_API_KEY`

**Network:**
- All VMs on the same VirtualBox Host-Only adapter
- Flask VM Adapter 2 set to NAT for outbound API access

---

## Running the pipeline

**1. Start the Flask target on the target VM:**
```bash
python vulnerable_llm_target.py
```
Confirm it's reachable: `curl http://<TARGET_IP>:5000/health`

**2. Run the red team pipeline from the attacker VM:**
```bash
python recon_vuln_agent_injection.py
```
Enter the DVWA IP and Flask target address when prompted. Review and
approve the proposed plan before exploitation runs.

**3. Run the blue team agent on the defender VM:**
```bash
python detection_agent_injection.py
```
Point it at `llm_target_access.log` on the target VM (mount or copy
the log, or point the agent at the target VM's `/log` endpoint).

---

## Ethical and legal notice

This project is for authorized security research in isolated lab
environments only. The tools, payloads, and techniques demonstrated here
are designed for use against intentionally vulnerable software
(DVWA, `vulnerable_llm_target.py`) that you control. Using these tools
against systems you do not own or have explicit written authorization to
test may constitute unauthorized access under applicable computer fraud
laws regardless of intent.
