import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "D:\Backup Files\Experiments\Compliance Evidence Pipeline"))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

import hashlib


USERS = {

    "admin": {

        "password":
            "admin123",

        "role":
            "Administrator",
    },


    "auditor": {

        "password":
            "audit123",

        "role":
            "Auditor",
    },


    "analyst": {

        "password":
            "analyst123",

        "role":
            "Analyst",
    },

}



def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()



def authenticate(
    username,
    password,
):

    if username not in USERS:

        return None


    user = USERS[username]


    if user["password"] == password:

        return {

            "username":
                username,

            "role":
                user["role"],

        }


    return None