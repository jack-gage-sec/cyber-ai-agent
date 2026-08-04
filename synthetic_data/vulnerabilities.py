import pandas as pd
import numpy as np
import random
from constants import (
    CVES,
    VULNERABILITY_STATUS,
    VULNERABILITY_STATUS_WEIGHTS,
)

def generate_vulnerabilities(number, hosts):

    vulnerabilities=[]

    for i in range(number):

        host = hosts.sample(1).iloc[0]

        cve = random.choice(CVES)

        vulnerability={

            "vulnerability_id":
                f"VULN{i:06d}",

            "hostname":
                host["hostname"],

            "cve":
                cve[0],

            "cvss":
                cve[1],

            "status":
                np.random.choice(
                    VULNERABILITY_STATUS,
    		    p=VULNERABILITY_STATUS_WEIGHTS,
                )

        }

        vulnerabilities.append(vulnerability)

    return pd.DataFrame(vulnerabilities)