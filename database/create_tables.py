import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "D:\Backup Files\Experiments\Compliance Evidence Pipeline"))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)



from database.connection import engine
from database.models import Base

print("Dropping existing tables...")
Base.metadata.drop_all(engine)

print("Creating tables...")
Base.metadata.create_all(engine)

print("Done.")