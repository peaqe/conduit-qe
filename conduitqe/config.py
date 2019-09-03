"""Configuration for working with rhsm-conduit."""

import os
import configparser
import logging
from types import SimpleNamespace

DEFAULT_CONFIG_PATHS = ['conduitqe.conf', '~/.conduitqe.conf']
CONDUIT_BASE_URL = 'http://localhost:8080'
INVENTORY_CI_BASE_URL = 'http://insights-inventory.platform-ci.svc:8080'
INVENTORY_QA_BASE_URL = 'http://insights-inventory.platform-qa.svc:8080'
INVENTORY_BASE_URL = INVENTORY_QA_BASE_URL
ENDPOINT_GET_FACTS = '/api/inventory/v1/hosts'
ENDPOINT_TRIGGER_UPDATE = '/r/insights/platform/rhsm-conduit/v1/inventories'
# Time (only in seconds) to wait for updates
CONDUITQE_WAIT_FOR_UPDATE_TIME = '30'
# Return logs newer than a relative duration like 60s or 2m
CONDUITQE_LOGS_SINCE_TIME = '1m'
# Number of attempts (from 1..max)
CONDUITQE_MAX_ATTEMPTS = 3

ConfigNamespace = None
logger = logging.getLogger(__name__)


def read_config_with_environ(filename):
    """Read config file and mix with environment variables."""
    conf = configparser.RawConfigParser(os.environ)
    with open(filename) as f:
        data = f.read()
        if '[DEFAULT]' not in data:
            data = '[DEFAULT]\n' + data
        conf.read_string(data)
    return conf


def find_config(paths):
    """Find a configuration file and read content."""
    conf = None
    for filename in paths:
        filename = os.path.expanduser(filename)
        filename = os.path.abspath(filename)
        logger.debug("Looking for configuration at '%s'", filename)
        if os.path.isfile(filename):
            logger.info("Using configuration '%s'", filename)
            conf = read_config_with_environ(filename)
            break
    return conf


def consolidate_config():
    """Consolidate configuration."""
    paths = DEFAULT_CONFIG_PATHS
    conduitqe_config = os.environ.get('CONDUITQE_CONFIG')
    if conduitqe_config:
        paths.insert(0, conduitqe_config)
    conf = find_config(paths)
    if conf is None:
        logger.warning('Configuration relying only on environment variables')
        conf = configparser.RawConfigParser(os.environ)
    return conf['DEFAULT']


def get_config():
    """Get configuration as a namespace."""
    global ConfigNamespace
    if ConfigNamespace is None:
        kwargs = consolidate_config()
        ConfigNamespace = SimpleNamespace(**kwargs)
        ConfigNamespace.conduit_base_url = get_conduit_base_url()
        ConfigNamespace.inventory_base_url = get_inventory_base_url()
        ConfigNamespace.endpoint_get_facts = os.getenv(
            'ENDPOINT_GET_FACTS', ENDPOINT_GET_FACTS)
        ConfigNamespace.endpoint_trigger_update = os.getenv(
            'ENDPOINT_TRIGGER_UPDATE', ENDPOINT_TRIGGER_UPDATE)
        ConfigNamespace.conduitqe_wait_for_update_time = os.getenv(
            'CONDUITQE_WAIT_FOR_UPDATE_TIME', CONDUITQE_WAIT_FOR_UPDATE_TIME)
        ConfigNamespace.conduitqe_logs_since_time = os.getenv(
            'CONDUITQE_LOGS_SINCE_TIME', CONDUITQE_LOGS_SINCE_TIME)
        ConfigNamespace.conduitqe_max_attempts = os.getenv(
            'CONDUITQE_MAX_ATTEMPTS', CONDUITQE_MAX_ATTEMPTS)
    return ConfigNamespace


def get_conduit_base_url():
    return os.getenv('CONDUIT_BASE_URL', CONDUIT_BASE_URL)


def get_inventory_base_url():
    return os.getenv('INVENTORY_BASE_URL', INVENTORY_BASE_URL)


def get_conduit_api_actuator():
    base_url = get_conduit_base_url()
    api_actuator = f'{base_url}/actuator'
    return api_actuator


def get_conduit_api_inventory():
    base_url = get_inventory_base_url()
    api_inventory = f'{base_url}/api/inventory/v1'
    return api_inventory
