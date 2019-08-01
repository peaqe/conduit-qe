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
import pytest
import oc


logger = logging.getLogger(__name__)


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
    valid_namespaces = ['rhsm', 'qpc']
    for result in data['results']:
        assert result['account'] == config.account_number
        assert result.get('facts'), result
        for fact in result['facts']:
            assert fact['namespace'] in valid_namespaces
            if fact['namespace'] == 'rhsm':
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
