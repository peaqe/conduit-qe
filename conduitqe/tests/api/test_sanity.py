"""Sanity Tests."""

import logging

from conduitqe import api

logger = logging.getLogger(__name__)


def test_conduit_version():
    status, resp = api.conduit_info()
    assert status == 200
    assert resp['build']['version'] == '1.0.0'


def test_conduit_health():
    status, resp = api.conduit_health()
    assert status == 200
    assert resp['status'] == 'UP'
