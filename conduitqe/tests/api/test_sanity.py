"""Sanity Tests."""

import logging

from conduitqe import api

logger = logging.getLogger(__name__)


def test_conduit_name_and_version():
    ok, data = api.conduit_info()
    assert ok, f'Conduit response with error: {data}'
    name = data['build']['name']
    assert name == 'rhsm-conduit', \
        f'Invalid name to test: {name}'
    version = data['build']['version']
    major, minor, patch_level = version.split('.')
    assert (major, minor) == ('1', '0'), \
        f'Invalid version to test: {major}.{minor}'


def test_conduit_health():
    ok, data = api.conduit_health()
    assert ok, f'Conduit response with error: {data}'
    assert data['status'] == 'UP', f'Bad status health: {data["status"]}'
