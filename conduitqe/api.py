"""API client for working with rhsm-conduit."""

import logging

import requests

logger = logging.getLogger(__name__)

CONDUIT_BASE_URL = 'http://localhost:8080/rhsm-conduit'
CONDUIT_API_VERSION = 'v1'
CONDUIT_API_URL = f'{CONDUIT_BASE_URL}/{CONDUIT_API_VERSION}'
CONDUIT_API_URL_STATUS = f'{CONDUIT_API_URL}/status'
CONDUIT_API_URL_AVAILABILITY = f'{CONDUIT_API_URL}/status/ready'


def conduit_version():
    logger.info(CONDUIT_API_URL_STATUS)
    resp = requests.get(CONDUIT_API_URL_STATUS)
    logger.info(resp)
    return resp.status_code, resp.json()


def conduit_availability():
    logger.info(CONDUIT_API_URL_AVAILABILITY)
    resp = requests.get(CONDUIT_API_URL_AVAILABILITY)
    logger.info(resp)
    return resp.status_code, resp.json()
