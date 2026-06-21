import requests
import re
import subprocess
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

dvwa_session = None

# ── DVWA Auto-Login ─────────────────────────────────────────────
def get_dvwa_session(target: str, username="admin", password="password"):
    """Login to DVWA programmatically and return an authenticated session."""
    session = requests.Session()

    login_page = session.get(f"http://{target}/dvwa/login.php")
    token_match = re.search(r"user_token['\"]\s+value=['\"]([a-f0-9]+)['\"]", login_page.text)
    if not token_match:
        print("[-] Could not find CSRF token on login page")
        return None
    user_token = token_match.group(1)

    login_response = session.post(
        f"http://{target}/dvwa/login.php",
        data={"username": username, "password": password,
              "Login": "Login", "user_token": user_token}
    )
    if "login.php" in login_response.url:
        print("[-] Login failed - check credentials")
        return None

    print(f"[+] Logged in. PHPSESSID: {session.cookies.get('PHPSESSID')}")

    security_page = session.get(f"http://{target}/dvwa/security.php")
    sec_token_match = re.search(r"user_token['\"]\s+value=['\"]([a-f0-9]+)['\"]", security_page.text)
    sec_token = sec_token_match.group(1) if sec_token_match else ""
    session.post(f"http://{target}/dvwa/security.php",
                  data={"security": "low", "seclev_submit": "Submit", "user_token": sec_token})
    session.cookies.set("security", "low")

    return session

# ── Recon Tools ──────────────────────────────────────────────────
@tool
def run_nmap(target: str) -> str:
    """Scan open ports and services on a target IP address."""
    result = subprocess.run(["nmap", "-sV", "-sC", "--open", target],
                             capture_output=True, text=True, timeout=120)
    return result.stdout

@tool
def run_gobuster(target: str) -> str:
    """Enumerate hidden directories and files on a web server."""
    result = subprocess.run(
        ["gobuster", "dir", "-u", f"http://{target}",
         "-w", "/usr/share/wordlists/dirb/common.txt", "-q"],
        capture_output=True, text=True, timeout=120)
    return result.stdout

@tool
def run_curl_headers(target: str) -> str:
    """Retrieve HTTP response headers from target."""
    result = subprocess.run(["curl", "-s", "-I", f"http://{target}"],
                             capture_output=True, text=True, timeout=30)
    return result.stdout

# ── Vulnerability Test Tools ──────────────────────────────────────
@tool
def test_sql_injection(target: str, payloads: str) -> str:
    """Test for SQL injection on DVWA. Payloads newline separated."""
    results = []
    for payload in [p.strip() for p in payloads.strip().split("\n") if p.strip()]:
        r = dvwa_session.get(f"http://{target}/dvwa/vulnerabilities/sqli/",
                              params={"id": payload, "Submit": "Submit"})
        if "First name" in r.text:
            results.append(f"VULNERABLE to payload: {payload}")
            for line in r.text.split("<br />"):
                if "First name" in line or "Surname" in line:
                    results.append(f"  Data: {line.replace('<pre>','').replace('</pre>','').strip()}")
        else:
            results.append(f"No result for payload: {payload}")
    return "\n".join(results)

@tool
def test_xss_reflected(target: str, payloads: str) -> str:
    """Test for reflected XSS on DVWA. Payloads newline separated."""
    results = []
    for payload in [p.strip() for p in payloads.strip().split("\n") if p.strip()]:
        r = dvwa_session.get(f"http://{target}/dvwa/vulnerabilities/xss_r/", params={"name": payload})
        results.append(f"VULNERABLE: {payload}" if payload in r.text else f"Filtered: {payload}")
    return "\n".join(results)

@tool
def test_command_injection(target: str, payloads: str) -> str:
    """Test for command injection on DVWA. Payloads newline separated."""
    results = []
    for payload in [p.strip() for p in payloads.strip().split("\n") if p.strip()]:
        r = dvwa_session.post(f"http://{target}/dvwa/vulnerabilities/exec/",
                               data={"ip": payload, "Submit": "Submit"})
        if any(k in r.text for k in ["root", "www-data", "uid=", "gid="]):
            results.append(f"VULNERABLE: {payload}")
            for line in r.text.split("<br />"):
                if any(k in line for k in ["root", "www-data", "uid=", "gid="]):
                    results.append(f"  Output: {line.replace('<pre>','').replace('</pre>','').strip()}")
        else:
            results.append(f"No execution: {payload}")
    return "\n".join(results)

@tool
def test_brute_force(target: str, credentials: str) -> str:
    """Test brute force on DVWA. Credentials newline separated username:password."""
    results = []
    for cred in [c.strip() for c in credentials.strip().split("\n") if c.strip()]:
        if ":" not in cred:
            continue
        u, p = cred.split(":", 1)
        r = dvwa_session.get(f"http://{target}/dvwa/vulnerabilities/brute/",
                              params={"username": u.strip(), "password": p.strip(), "Login": "Login"})
        results.append(f"VALID: {u}:{p}" if "Welcome to the password protected area" in r.text else f"Invalid: {u}:{p}")
    return "\n".join(results)

@tool
def test_file_inclusion(target: str, payloads: str) -> str:
    """Test for LFI on DVWA. Payloads newline separated."""
    results = []
    for payload in [p.strip() for p in payloads.strip().split("\n") if p.strip()]:
        r = dvwa_session.get(f"http://{target}/dvwa/vulnerabilities/fi/", params={"page": payload})
        results.append(f"VULNERABLE: {payload}" if "root:x" in r.text else f"Not vulnerable: {payload}")
    return "\n".join(results)

@tool
def login_to_dvwa(target: str) -> str:
    """Log into DVWA and establish an authenticated session for vulnerability testing."""
    global dvwa_session
    dvwa_session = get_dvwa_session(target)
    if dvwa_session is None:
        return "Login failed - cannot proceed with vulnerability testing"
    return "Login successful - authenticated session established, security set to low"

# ── Agent Setup ──────────────────────────────────────────────────
recon_tools = [run_nmap, run_gobuster, run_curl_headers]
vuln_tools = [login_to_dvwa, test_sql_injection, test_xss_reflected,
              test_command_injection, test_brute_force, test_file_inclusion]

llm = ChatAnthropic(model="claude-sonnet-4-5", temperature=0)

recon_agent = create_react_agent(llm, recon_tools)
vuln_agent = create_react_agent(llm, vuln_tools)

def run_recon_phase(target_ip: str) -> str:
    prompt = f"""
    Perform reconnaissance on {target_ip}: port scanning, directory enumeration,
    and header grabbing. Summarize what services, paths, and technologies were found.
    Only target {target_ip}.
    """
    print("\n=== PHASE 1: RECON ===\n")
    result = recon_agent.invoke({"messages": [HumanMessage(content=prompt)]})
    output = result["messages"][-1].content
    print(output)
    return output

def get_exploitation_plan(target_ip: str, recon_findings: str) -> str:
    """Ask Claude to propose which vulnerabilities to test, without executing anything yet."""
    prompt = f"""
    Based on this recon data for {target_ip}, propose a vulnerability testing plan.

    Recon findings:
    {recon_findings}

    For each vulnerability category you recommend testing (from: SQL Injection,
    Reflected XSS, Command Injection, Brute Force, File Inclusion), state:
    - Why it's worth testing given the recon findings
    - What kind of payloads you'd use (describe the approach, not the full list yet)

    Do not call any tools. Just describe the plan in plain text.
    """
    result = llm.invoke([HumanMessage(content=prompt)])
    return result.content

def run_vuln_phase(target_ip: str, approved_plan: str) -> str:
    prompt = f"""
    You are testing DVWA at {target_ip} in an authorized lab engagement.
    The user has reviewed and approved the following exploitation plan:

    {approved_plan}

    Call login_to_dvwa first. Then generate payloads/credentials for each
    approved vulnerability category and call the matching test tool, passing
    payloads as newline separated strings.

    Produce a final report: which vulnerabilities were confirmed, what data
    was exposed, risk, and remediation.

    Only target {target_ip}.
    """
    print("\n=== PHASE 3: EXPLOITATION ===\n")
    result = vuln_agent.invoke({"messages": [HumanMessage(content=prompt)]})
    output = result["messages"][-1].content
    print(output)
    return output

def run_pipeline(target_ip: str):
    # Phase 1: Recon (runs automatically, read-only)
    recon_findings = run_recon_phase(target_ip)

    # Phase 2: Propose plan, get human approval
    print("\n=== PHASE 2: PROPOSED EXPLOITATION PLAN ===\n")
    plan = get_exploitation_plan(target_ip, recon_findings)
    print(plan)

    print("\n" + "=" * 60)
    approval = input("\nApprove this plan and proceed with exploitation? (yes/no): ").strip().lower()

    if approval not in ("yes", "y"):
        print("\n[-] Exploitation cancelled by user. Recon findings saved, no attacks were run.")
        with open("pipeline_report.txt", "w") as f:
            f.write("=== RECON FINDINGS ===\n" + recon_findings +
                    "\n\n=== PROPOSED PLAN (NOT EXECUTED) ===\n" + plan)
        return

    # Phase 3: Run only after explicit approval
    vuln_report = run_vuln_phase(target_ip, plan)

    full_report = (
        "=== RECON FINDINGS ===\n" + recon_findings +
        "\n\n=== APPROVED PLAN ===\n" + plan +
        "\n\n=== EXPLOITATION REPORT ===\n" + vuln_report
    )
    with open("pipeline_report.txt", "w") as f:
        f.write(full_report)
    print("\nFull report saved to pipeline_report.txt")

if __name__ == "__main__":
    target = input("Enter DVWA IP: ")
    run_pipeline(target)
