"""API client for working with rhsm-conduit."""

import logging

import requests
from conduitqe.config import (
        get_conduit_api_actuator,
        get_conduit_api_inventory
)
from conduitqe.utils import create_authentication

logger = logging.getLogger(__name__)

CONDUIT_API_ACTUATOR = get_conduit_api_actuator()
CONDUIT_API_INVENTORY = get_conduit_api_inventory()


def conduit_info():
    url = f'{CONDUIT_API_ACTUATOR}/info'
    logger.info(url)
    resp = requests.get(url)
    logger.info(resp)
    return resp.status_code, resp.json()


def conduit_health():
    url = f'{CONDUIT_API_ACTUATOR}/health'
    logger.info(url)
    resp = requests.get(url)
    logger.info(resp)
    return resp.status_code, resp.json()


def conduit_host_inventory(account_number):
    auth = create_authentication(account_number)
    headers = {'x-rh-identity': auth}
    url = f'{CONDUIT_API_INVENTORY}/hosts'
    logger.info(url)
    resp = requests.get(url, headers=headers)
    logger.info(resp)
    return resp.status_code, resp.json()
