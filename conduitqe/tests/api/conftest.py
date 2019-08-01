"""Pytest customizations and fixtures for the RHSM-conduit tests."""

import logging
import json
import pytest
import oc

from conduitqe.config import get_config
from conduitqe.utils import create_authentication


logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def config():
    """Get configuration with environment variables (all in lowercase)."""
    cfg = get_config()
    return cfg


@pytest.fixture(scope="module")
def rhsm_conduit_instance(config):
    """Get/guess running rhsm-conduit instance."""
    if hasattr(config, 'conduit_pod'):
        return config.conduit_pod
    conduit = None
    output = oc.get_pods()
    pods = [x.split() for x in output[1:]]
    for pod in pods:
        if pod[0].startswith('rhsm-conduit-quartz-postgresql'):
            continue
        if pod[2] == 'Running' and pod[0].startswith('rhsm-conduit-'):
            conduit = pod[0]
    logger.debug('rhsm-conduit instance %s', conduit)
    return conduit


@pytest.fixture(scope="module")
def openshift_setup(config):
    """Do login on Openshift and set the project."""
    oc.login(config.openshift_url, config.openshift_token)
    result = oc.set_project(config.openshift_project)
    return result


@pytest.fixture(scope="module")
def rh_identity(config):
    """Create the authentication header."""
    auth = create_authentication(config.account_number)
    header = f'x-rh-identity: {auth}'
    logger.debug('rh-identity %s', header)
    return header


@pytest.fixture()
def hosts_inventory(config, rhsm_conduit_instance, rh_identity):
    """Get Insights hosts inventory information in JSON."""
    url = f'{config.inventory_base_url}{config.endpoint_get_facts}'
    cmd = f'curl -s -H "{rh_identity}" {url}'
    output = oc.exec(rhsm_conduit_instance, cmd)
    output = ''.join(output)
    logger.debug('hosts inventory %s', output)
    data = json.loads(output)
    return data
