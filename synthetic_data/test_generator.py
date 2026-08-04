from users import generate_users
from export import export_csv

users = generate_users(500)

export_csv(
    users,
    "users.csv"
)