"""Unit tests for utilities."""

from conduitqe import utils


def test_authentication():
    account_number = 123456789
    expected = b'eyJpZGVudGlmeSI6IHsiYWNjb3VudF9udW1iZXIiOiAiMTIzNDU2Nzg5In19'
    auth = utils.create_authentication(account_number)
    assert auth == expected
