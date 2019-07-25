"""Configuration for working with rhsm-conduit."""

import os
import configparser
import logging
from types import SimpleNamespace

CONFIG_PATHS = ['conduitqe.conf', '~/.conduitqe.conf']
CONDUIT_BASE_URL = 'http://localhost:8080'
INVENTORY_CI_BASE_URL = 'http://insights-inventory.platform-ci.svc:8080'
INVENTORY_QA_BASE_URL = 'http://insights-inventory.platform-qa.svc:8080'
INVENTORY_BASE_URL = INVENTORY_QA_BASE_URL
ENDPOINT_GET_FACTS = '/api/inventory/v1/hosts'
ENDPOINT_TRIGGER_UPDATE = '/r/insights/platform/rhsm-conduit/v1/inventories'

ConfigNamespace = None
logger = logging.getLogger(__name__)


def read_conf_file_with_environ(filename):
    """Read config file and mix with environment variables."""
    conf = configparser.ConfigParser(os.environ)
    with open(filename) as f:
        conf.read_string('[DEFAULT]\n' + f.read())
    return conf


def consolidate_configs():
    """Find a configuration file and consolidate with environ vars."""
    conf = None
    for filename in CONFIG_PATHS:
        filename = os.path.expanduser(filename)
        if os.path.isfile(filename):
            logger.debug("Reading configuration on '%s'", filename)
            conf = read_conf_file_with_environ(filename)
            break
    if conf is None:
        logger.debug('Configuration relying only on environment variables')
        conf = configparser.ConfigParser(os.environ)
    return conf['DEFAULT']


def get_config():
    """Get configuration."""
    global ConfigNamespace
    if ConfigNamespace is None:
        kwargs = consolidate_configs()
        ConfigNamespace = SimpleNamespace(**kwargs)
        ConfigNamespace.conduit_base_url = get_conduit_base_url()
        ConfigNamespace.inventory_base_url = get_inventory_base_url()
        ConfigNamespace.endpoint_get_facts = os.getenv(
            'ENDPOINT_GET_FACTS', ENDPOINT_GET_FACTS)
        ConfigNamespace.endpoint_trigger_update = os.getenv(
            'ENDPOINT_TRIGGER_UPDATE', ENDPOINT_TRIGGER_UPDATE)
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
