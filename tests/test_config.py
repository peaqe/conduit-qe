"""Tests for configuration."""

from conduitqe import config


def test_singleton_config_space():
    cfg1 = config.get_config()
    cfg1.name = 'test'
    cfg2 = config.get_config()
    cfg2.number = 123
    assert cfg1.name == cfg2.name
    assert cfg1.number == cfg2.number
