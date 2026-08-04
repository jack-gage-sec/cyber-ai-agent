import os
import sys

from pathlib import Path

dir_above_cep = Path(__file__).resolve().parents[2]
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), dir_above_cep))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

import hashlib


USERS = {

    "admin": {

        "password":
            "{theadminpassword}",

        "role":
            "Administrator",
    },


    "auditor": {

        "password":
            "{theauditpassword}",

        "role":
            "Auditor",
    },


    "analyst": {

        "password":
            "{theanalystpassword}",

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
