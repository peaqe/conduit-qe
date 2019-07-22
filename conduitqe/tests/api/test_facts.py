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
    match = False
    for log in logs:
        data = json.loads(log)
        message = data.get('message', '')
        logger.debug("message '%s' with text '%s' and org_key '%s'",
                     message, text, org_key)
        if message and message.startswith(text):
            if org_key in data['message']:
                match = True
                break
    return match


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
    endpoint = f'/r/insights/platform/rhsm-conduit/v1/inventories/{org_key}'
    url = f'{config.conduit_base_url}{endpoint}'
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
