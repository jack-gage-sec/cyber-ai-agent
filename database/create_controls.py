import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "D:\Backup Files\Experiments\Compliance Evidence Pipeline"))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

from database.connection import engine
from database.models import Base


Base.metadata.create_all(
    bind=engine
)

print(
    "Database tables created."
)