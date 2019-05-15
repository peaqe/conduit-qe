"""Unit tests for utilities."""

from conduitqe import utils


def test_authentication():
    org_key = 123456789
    expected = b'eyJpZGVudGlmeSI6IHsiYWNjb3VudF9udW1iZXIiOiAiMTIzNDU2Nzg5In19'
    auth = utils.create_authentication(org_key)
    assert auth == expected
