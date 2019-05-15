"""API client for working with rhsm-conduit."""

import logging

import requests
from conduitqe.config import get_conduit_api_actuator

logger = logging.getLogger(__name__)

CONDUIT_API_ACTUATOR = get_conduit_api_actuator()


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
