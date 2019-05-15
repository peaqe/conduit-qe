"""Utilities for rhsm-conduit."""

import json
import base64


def create_authentication(org_key):
    if type(org_key) is int:
        org_key = str(org_key)
    auth = {'identify': {'account_number': org_key}}
    auth = json.dumps(auth)
    auth = base64.standard_b64encode(auth.encode('utf8'))
    return auth
