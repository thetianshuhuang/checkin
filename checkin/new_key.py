
"""Script for creating a secret key

Attributes
----------
CHARS : str
    Valid characters for a django secret key: a-z, 0-9, !@#$%^&*(-_=+)
    (No capitals)
"""

import secrets
import json


CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'


def new_key(target="key.json"):
    """Generate a new key file, in the form of a JSON with one entry (``key``).

    Parameters
    ----------
    target : str
        Name of the file to generate; defaults to key.json
    """

    key = "".join([secrets.choice(CHARS) for i in range(50)])
    print("Created new secret key: " + key)

    with open(target, "w+") as keyfile:
        keyfile.write(json.dumps({"key": key}))


if __name__ == '__main__':
    new_key()
