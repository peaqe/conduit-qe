"""Unit tests for the API client."""

from unittest import mock
from conduitqe import api


def test_conduit_good_response():
    response = mock.Mock()
    response.status_code = 200
    api.request = mock.MagicMock(return_value=response)
    ok, data = api.conduit('/info')
    assert ok


def test_conduit_bad_response():
    response = mock.Mock()
    response.status_code = 404
    api.request = mock.MagicMock(return_value=response)
    ok, data = api.conduit('/xyz')
    assert not ok
