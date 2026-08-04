from users import generate_users
from hosts import generate_hosts
from vulnerabilities import generate_vulnerabilities
from alerts import generate_alerts
from export import export_csv
from access_reviews import generate_access_reviews
from policy_exceptions import generate_policy_exceptions
from control_tests import generate_control_tests
from evidence_generator import generate_evidence


users = generate_users(500)

hosts = generate_hosts(
    1000,
    users
)


vulnerabilities = generate_vulnerabilities(
    5000,
    hosts
)

alerts = generate_alerts(
    50000,
    users,
    hosts
)

access_reviews = generate_access_reviews(
    2000,
    users
)

policy_exceptions = generate_policy_exceptions(
    500,
    users
)

control_tests = generate_control_tests(
    1000,
    access_reviews,
    policy_exceptions
)

generate_evidence(
    control_tests
)


export_csv(users,"users.csv")

export_csv(hosts,"hosts.csv")

export_csv(alerts, "alerts.csv")

export_csv(access_reviews, "access_reviews.csv")

export_csv(policy_exceptions, "policy_exceptions.csv")

export_csv(control_tests, "control_tests.csv")

export_csv(
    vulnerabilities,
    "vulnerabilities.csv"
)


print("Synthetic data generation complete")