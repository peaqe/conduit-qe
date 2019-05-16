"""Configuration for working with rhsm-conduit."""

import os

CONDUIT_BASE_URL = 'http://localhost:8080'
INVENTORY_BASE_URL = 'http://insights-inventory.platform-qa.svc:8080'


def get_conduit_base_url():
    return os.getenv('CONDUIT_BASE_URL', CONDUIT_BASE_URL)


def get_inventory_base_url():
    return os.getenv('INVENTORY_BASE_URL', INVENTORY_BASE_URL)


def get_conduit_api_actuator():
    base_url = get_conduit_base_url()
    api_actuator = f'{base_url}/actuator'
    return api_actuator


def get_conduit_api_inventory():
    base_url = get_inventory_base_url()
    api_inventory = f'{base_url}/api/inventory/v1'
    return api_inventory
