import re
import time
from collections import defaultdict
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import subprocess

load_dotenv()

# ── Detection Signatures ───────────────────────────────────────
SIGNATURES = {
    "sql_injection": [
        r"'.*OR.*'",
        r"UNION.*SELECT",
        r"1=1",
        r"--\s*$",
        r"'.*--",
        r"information_schema",
        r"concat\(",
    ],
    "xss": [
        r"<script>",
        r"onerror=",
        r"onload=",
        r"javascript:",
        r"alert\(",
    ],
    "command_injection": [
        r";\s*whoami",
        r";\s*id",
        r"\|\s*cat",
        r"&&\s*cat",
        r"/etc/passwd",
    ],
    "lfi": [
        r"\.\./",
        r"\.\.\\",
        r"/etc/passwd",
        r"/etc/hosts",
    ],
    "brute_force": [
        r"username=.*&password=",
    ]
}

# ── Track Request Counts Per IP ────────────────────────────────
request_counts = defaultdict(int)
alerts = []

# ── Tools ──────────────────────────────────────────────────────
@tool
def read_apache_logs(log_file: str) -> str:
    """Read and return the contents of an Apache log file."""
    try:
        with open(log_file, "r") as f:
            lines = f.readlines()
            # Return last 100 lines
            return "".join(lines[-100:])
    except FileNotFoundError:
        return f"Log file not found: {log_file}"
    except PermissionError:
        return f"Permission denied reading: {log_file}"

@tool
def analyze_log_for_attacks(log_content: str) -> str:
    """Analyze log content for attack signatures and return findings."""
    findings = []
    request_counts = defaultdict(int)

    for line in log_content.split("\n"):
        if not line.strip():
            continue

        # Extract IP address
        ip_match = re.match(r"(\d+\.\d+\.\d+\.\d+)", line)
        ip = ip_match.group(1) if ip_match else "unknown"
        request_counts[ip] += 1

        # Check each attack signature
        for attack_type, patterns in SIGNATURES.items():
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append(
                        f"[ALERT] {attack_type.upper()} detected from {ip}: {line.strip()[:200]}"
                    )
                    break

    # Check for brute force by request volume
    for ip, count in request_counts.items():
        if count > 20:
            findings.append(
                f"[ALERT] POSSIBLE BRUTE FORCE from {ip}: {count} requests detected"
            )

    if not findings:
        return "No attacks detected in log sample"

    return "\n".join(findings)

@tool
def get_unique_ips(log_content: str) -> str:
    """Extract and count unique IP addresses from log content."""
    ip_counts = defaultdict(int)

    for line in log_content.split("\n"):
        ip_match = re.match(r"(\d+\.\d+\.\d+\.\d+)", line)
        if ip_match:
            ip_counts[ip_match.group(1)] += 1

    result = []
    for ip, count in sorted(ip_counts.items(), key=lambda x: x[1], reverse=True):
        result.append(f"IP: {ip} - {count} requests")

    return "\n".join(result) if result else "No IPs found"

@tool
def get_suspicious_urls(log_content: str) -> str:
    """Extract URLs containing suspicious characters or patterns."""
    suspicious = []
    suspicious_chars = ["'", "<script>", "../", "UNION", "SELECT", "OR 1=1", "whoami"]

    for line in log_content.split("\n"):
        if any(char.lower() in line.lower() for char in suspicious_chars):
            suspicious.append(line.strip()[:300])

    return "\n".join(suspicious) if suspicious else "No suspicious URLs found"

@tool 
def generate_alert_report(findings: str) -> str:
    """Format findings into a structured alert report."""
    report = []
    report.append("=" * 50)
    report.append("INTRUSION DETECTION REPORT")
    report.append("=" * 50)

    # Count alerts by type
    alert_types = defaultdict(int)
    for line in findings.split("\n"):
        if "[ALERT]" in line:
            for attack_type in SIGNATURES.keys():
                if attack_type.upper() in line:
                    alert_types[attack_type] += 1

    report.append("\nALERT SUMMARY:")
    for attack_type, count in alert_types.items():
        report.append(f"  {attack_type.upper()}: {count} alerts")

    report.append("\nDETAILED FINDINGS:")
    report.append(findings)
    report.append("=" * 50)

    return "\n".join(report)

# ── Agent Setup ────────────────────────────────────────────────
tools = [
    read_apache_logs,
    analyze_log_for_attacks,
    get_unique_ips,
    get_suspicious_urls,
    generate_alert_report
]

llm = ChatAnthropic(
    model="claude-sonnet-4-5",
    temperature=0
)

agent = create_react_agent(llm, tools)

def run_detection(log_file: str):
    prompt = f"""
    You are a security detection agent monitoring a web server for attacks.
    Analyze the Apache log file at: {log_file}

    Follow this process:
    1. Read the log file contents
    2. Extract all unique IP addresses and their request counts
    3. Find all suspicious URLs containing attack patterns
    4. Analyze the logs for attack signatures including:
       - SQL injection attempts
       - XSS attempts
       - Command injection attempts
       - Local file inclusion attempts
       - Brute force attempts (high request volume)
    5. Generate a structured alert report with:
       - Summary of detected attack types
       - Source IP addresses of attackers
       - Specific attack payloads used
       - Timeline of the attack
       - Recommended defensive actions

    Be thorough and flag anything that looks suspicious.
    """

    print("\n=== STARTING DETECTION AGENT ===\n")

    result = agent.invoke({
        "messages": [HumanMessage(content=prompt)]
    })

    final_output = result["messages"][-1].content

    print("\n=== DETECTION REPORT ===")
    print(final_output)

    with open("detection_report.txt", "w") as f:
        f.write(final_output)
    print("\nReport saved to detection_report.txt")

if __name__ == "__main__":
    log_file = input("Enter path to Apache log file (default: /var/log/apache2/access.log): ")
    if not log_file:
        log_file = "/var/log/apache2/access.log"
    run_detection(log_file)