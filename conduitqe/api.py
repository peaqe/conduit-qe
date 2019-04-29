"""API client for working with rhsm-conduit."""

import logging

import requests

logger = logging.getLogger(__name__)

CONDUIT_BASE_URL = 'http://localhost:8080'
CONDUIT_API_ACTUATOR = f'{CONDUIT_BASE_URL}/actuator'


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
