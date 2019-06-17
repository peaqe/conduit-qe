"""Sanity Tests."""

import logging

from conduitqe import api

logger = logging.getLogger(__name__)


def test_conduit_version():
    status, resp = api.conduit_info()
    assert status == 200, f'Conduit response with error: {status}'
    version = resp['build']['version']
    logger.info(f'Conduit version reported is {version}')
    major, minor, patch_level = version.split('.')
    assert (major, minor) == ('1', '0'), \
        f'Invalid version to test: {major}.{minor}'


def test_conduit_health():
    status, resp = api.conduit_health()
    assert status == 200, f'Conduit response with error: {status}'
    assert resp['status'] == 'UP', f'Bad status health: {resp["status"]}'
