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
    response = requests.request(method, url, **kwargs)
    return response


def parse(response):
    if 200 <= response.status_code < 400:
        return True, response.json()
    return False, response.text


def conduit(endpoint):
    try:
        url = f'{CONDUIT_API_ACTUATOR}{endpoint}'
        response = request('get', url)
    except requests.exceptions.ConnectionError as err:
        return False, err
    return parse(response)


def conduit_info():
    return conduit('/info')


def conduit_health():
    return conduit('/health')


def conduit_host_inventory(account_number):
    auth = create_authentication(account_number)
    headers = {'x-rh-identity': auth}
    url = f'{CONDUIT_API_INVENTORY}/hosts'
    response = request('get', url, headers=headers)
    return parse(response)
