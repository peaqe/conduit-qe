"""Sanity Tests."""

import logging

from conduitqe import api

logger = logging.getLogger(__name__)


def test_status_version():
    status, resp = api.conduit_version()
    assert status == 200
    assert resp['version'] == '1.0.0'


def test_status_availability():
    status, resp = api.conduit_availability()
    assert status == 200
    assert resp['availability'] == 'OK'
