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


def request(method, url, **kwargs):
    logger.debug(f'method={method}, url={url}')
    resp = requests.request(method, url, **kwargs)
    logger.debug(f'response={resp.status_code}, text={resp.text}')
    return resp


def conduit_info():
    url = f'{CONDUIT_API_ACTUATOR}/info'
    resp = request('get', url)
    return resp.status_code, resp.json()


def conduit_health():
    url = f'{CONDUIT_API_ACTUATOR}/health'
    resp = request('get', url)
    return resp.status_code, resp.json()


def conduit_host_inventory(account_number):
    auth = create_authentication(account_number)
    headers = {'x-rh-identity': auth}
    url = f'{CONDUIT_API_INVENTORY}/hosts'
    resp = request('get', url, headers=headers)
    return resp.status_code, resp.json()
