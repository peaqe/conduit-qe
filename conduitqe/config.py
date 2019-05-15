"""Configuration for working with rhsm-conduit."""

import os

CONDUIT_BASE_URL = 'http://localhost:8080'


def get_conduit_base_url():
    return os.getenv('CONDUIT_BASE_URL', CONDUIT_BASE_URL)


def get_conduit_api_actuator():
    base_url = get_conduit_base_url()
    api_actuator = f'{base_url}/actuator'
    return api_actuator
