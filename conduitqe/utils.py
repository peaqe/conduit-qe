"""Utilities for using rhsm-conduit."""

import json
import base64
import logging


logger = logging.getLogger(__name__)


def create_authentication(account_number):
    """Create authentication with account number."""
    if type(account_number) is int:
        account_number = str(account_number)
    auth = {'identity': {'account_number': account_number}}
    auth = json.dumps(auth)
    auth = base64.standard_b64encode(auth.encode('utf8'))
    auth = auth.decode('utf8')
    logger.debug(auth)
    return auth
