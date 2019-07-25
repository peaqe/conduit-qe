"""Tests for triggering facts updates.

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
    return config.conduit_pod


@pytest.fixture(scope="module")
def openshift_setup(config):
    oc.login(config.openshift_url, config.openshift_token)
    result = oc.set_project(config.project)
    return result


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
def test_check_basic_facts(config, rhsm_conduit_instance):
    """Test checking basic hosts facts (sanity test).
    :id: 4b7744b8-ad7a-11e9-aed1-acde48001122
    :description: Test when checking basic host facts if
        the most basic facts elements are present.
    :expectedresults: we get a valid JSON (possible with pagination),
        where we have basic facts for the hosts that belongs to an account.
    """
    auth = create_authentication(config.account_number)
    url = f'{config.inventory_base_url}{config.endpoint_get_facts}'
    header = f'x-rh-identity: {auth}'
    cmd = f'curl -s -H "{header}" {url}'
    output = oc.exec(rhsm_conduit_instance, cmd)
    assert '!DOCTYPE' not in output[0], '\n'.join(output)
    output = ''.join(output)
    data = json.loads(output)
    assert data.get('results', ''), output
    # FIXME: pagination, 'total': 8, 'count': 8, 'page': 1, 'per_page': 50
    for result in data['results']:
        assert result.get('facts'), result
        for fact in result['facts']:
            assert fact['namespace'] == 'rhsm'
            assert fact['facts']['orgId'] == config.org_id
