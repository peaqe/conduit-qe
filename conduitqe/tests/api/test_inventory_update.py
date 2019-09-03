"""Tests for Inventory Service updates.

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


logger = logging.getLogger(__name__)


def lookup_in_logs(logs, text, org_key):
    """Look up text in logs for matching org_key."""
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
    logs = oc.logs(rhsm_conduit_instance,
                   since=config.conduitqe_logs_since_time)
    updating = lookup_in_logs(logs, 'Updating inventory', org_key)
    assert updating, f'Updating inventory has failed for org key {org_key}'
    time.sleep(int(config.conduitqe_wait_for_update_time))
    # Host inventory update completed look-up
    n = 1
    while n <= config.conduitqe_max_attempts:
        logger.info('Attempt %d of %d to inventory update complete',
                    n, config.conduitqe_max_attempts)
        logs = oc.logs(rhsm_conduit_instance,
                       since=config.conduitqe_logs_since_time)
        updated = lookup_in_logs(logs,
                                 'Host inventory update completed', org_key)
        if updated:
            break
        n += 1
    assert updated, \
        f'Host inventory update not completed for org key {org_key}'
