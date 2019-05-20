"""Utilities for rhsm-conduit."""

import json
import base64


def create_authentication(account_number):
    if type(account_number) is int:
        account_number = str(account_number)
    auth = {'identify': {'account_number': account_number}}
    auth = json.dumps(auth)
    auth = base64.standard_b64encode(auth.encode('utf8'))
    return auth
