"""Tests for Inventory Service Facts.

:caseautomation: automated
:casecomponent: api
:caseimportance: high
:caselevel: integration
:requirement: rhsm-conduit
:testtype: functional
:upstream: yes
"""

import logging
import json
import time
import pytest
import oc

from conduitqe.config import get_config
from conduitqe.utils import create_authentication


logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def config():
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
    oc.login(config.openshift_url, config.openshift_token)
    result = oc.set_project(config.openshift_project)
    return result


@pytest.fixture(scope="module")
def rh_identity(config):
    auth = create_authentication(config.account_number)
    header = f'x-rh-identity: {auth}'
    return header


@pytest.fixture()
def hosts_inventory(config, rhsm_conduit_instance, rh_identity):
    url = f'{config.inventory_base_url}{config.endpoint_get_facts}'
    cmd = f'curl -s -H "{rh_identity}" {url}'
    output = oc.exec(rhsm_conduit_instance, cmd)
    output = ''.join(output)
    data = json.loads(output)
    return data


@pytest.mark.openshift
def test_conduit_is_running(openshift_setup, rhsm_conduit_instance):
    """Test if a given conduit instance is up and running.

    :id: b082bdae-aca5-11e9-ab30-acde4800112
    :description: Ensure that a given conduit instance is up and running.
    :expectedresults: Running the command `uptime` returns the system is up
        (it doesn't matter for how long).
    """
    output = oc.exec(rhsm_conduit_instance, 'uptime')
    assert ' up ' in output[0]


def lookup_in_logs(logs, text, org_key):
    """Look up text in logs for matching org_key.
    """
    for log in logs:
        data = json.loads(log)
        message = data.get('message', '')
        logger.debug("message '%s' with text '%s' and org_key '%s'",
                     message, text, org_key)
        if message and message.startswith(text):
            if org_key in data['message']:
                return True
    return False


@pytest.mark.openshift
def test_trigger_inventory_update(config, rhsm_conduit_instance):
    """Test triggering simple inventory update.
    :id: 4e92aafa-aca8-11e9-b0e7-acde48001122
    :description: Test that triggering a simple inventory update, without
        changing any machine's facts, should result in success.
    :expectedresults: inspecting the conduit logs should indicate that
        the org key is presented and the system was successfully updated.
    """
    org_key = config.org_id
    endpoint_trigger_update = f'{config.endpoint_trigger_update}/{org_key}'
    url = f'{config.conduit_base_url}{endpoint_trigger_update}'
    cmd = f'curl -s -I -X POST {url}'
    output = oc.exec(rhsm_conduit_instance, cmd)
    assert output[0].startswith('HTTP/1.1 204'), '\n'.join(output)
    # Updating inventory look-up
    logs = oc.logs(rhsm_conduit_instance, since='1m')
    updating = lookup_in_logs(logs, 'Updating inventory', org_key)
    assert updating, f'Updating inventory has failed for org key {org_key}'
    time.sleep(5)
    # Host inventory update completed look-up
    logs = oc.logs(rhsm_conduit_instance, since='1m')
    updated = lookup_in_logs(logs, 'Host inventory update completed', org_key)
    assert updated, \
        f'Host inventory update not completed for org key {org_key}'


@pytest.mark.openshift
def test_basic_facts(config, rhsm_conduit_instance, rh_identity):
    """Test checking basic hosts facts (sanity test).
    :id: 4b7744b8-ad7a-11e9-aed1-acde48001122
    :description: Test when checking basic host facts if
        the most basic facts elements are present.
    :expectedresults: we get a valid JSON (possible with pagination),
        where we have basic facts for the hosts that belongs to an account.
    """
    url = f'{config.inventory_base_url}{config.endpoint_get_facts}'
    cmd = f'curl -s -H "{rh_identity}" {url}'
    output = oc.exec(rhsm_conduit_instance, cmd)
    assert '!DOCTYPE' not in output[0], '\n'.join(output)
    output = ''.join(output)
    data = json.loads(output)
    assert data.get('results', ''), output
    # FIXME: pagination, 'total': 8, 'count': 8, 'page': 1, 'per_page': 50
    for result in data['results']:
        assert result['account'] == config.account_number
        assert result.get('facts'), result
        for fact in result['facts']:
            assert fact['namespace'] == 'rhsm'
            assert fact['facts']['orgId'] == config.org_id


@pytest.mark.openshift
def test_canonical_facts(hosts_inventory):
    """Test checking the canonical facts.
    :id: 8b034b7a-b3d8-11e9-976b-acde48001122
    :description: Test if the canonical facts are present.
    :expectedresults: all the expected canonical facts are present.
    """
    expected_facts = [
        'insights_id', 'rhel_machine_id', 'subscription_manager_id',
        'satellite_id', 'external_id', 'bios_uuid', 'ip_addresses',
        'fqdn', 'mac_addresses', 'display_name', 'ansible_host']
    for result in hosts_inventory['results']:
        for expected_fact in expected_facts:
            assert expected_fact in result


@pytest.mark.openshift
def test_rshm_namespace_facts(hosts_inventory):
    """Test checking the RHSM namespace definition facts.
    :id: 8b034b7a-b3d8-11e9-976b-acde48001122
    :description: Test if facts under the RHSM namespace are present.
    :expectedresults: all the expected rhsm facts are present.
    """
    expected_facts = [
        'MEMORY', 'RH_PROD', 'CPU_CORES', 'IS_VIRTUAL',
        'CPU_SOCKETS', 'ARCHITECTURE']
    for result in hosts_inventory['results']:
        for fact in result['facts']:
            if fact['namespace'] == 'rhsm':
                for expected_fact in expected_facts:
                    assert expected_fact in fact['facts']


@pytest.mark.openshift
def test_qpc_namespace_facts(hosts_inventory):
    """Test checking the QPC namespace definition facts.
    :id: f7575dbd-b468-11e9-a9f0-acde48001122
    :description: Test if facts under the QPC namespace are present.
    :expectedresults: all the expected qpc facts are present.
    """
    expected_facts = ['rh_products_installed', 'rh_product_certs']
    for result in hosts_inventory['results']:
        for fact in result['facts']:
            if fact['namespace'] == 'qpc':
                for expected_fact in expected_facts:
                    assert expected_fact in fact['facts']
