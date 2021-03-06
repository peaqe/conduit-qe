#!/bin/sh
#
# Conduit-qe utilities.
#

CONDUITQE_CONF="${HOME}/.conduitqe.conf"
CUSTOM_FACTS="/etc/rhsm/facts/custom.facts"

usage()
{
	cat <<EOF
Usage: $0 [OPTIONS] [COMMANDS] ...

Available values for OPTIONS include:

  -c, --config PATH select configuration file

Available values for COMMANDS include:

  auth, identity      show authentication token from account number
  register            register system
  facts, update-facts trigger facts update
  hosts, inventories  show systems inventories in JSON format
  logs, watch-logs    follow rhsm-conduit logs
  pod, conduit-pod    guess running rhsm-conduit pod name

EOF
	exit 1
}

get_conduit_pod()
{
	oc project ${OPENSHIFT_PROJECT} > /dev/null
	oc get pods | sed -n '/^rhsm-conduit-[0-9]/p' | grep Running  | awk '{ print $1 }'
}

read_config()
{
	if test -f "${CONDUITQE_CONF}"; then
		source "${CONDUITQE_CONF}"
	else
		echo "Configuration file not found: ${CONDUITQE_CONF}"
		exit 1
	fi
	AUTHENTICATION=$(printf '{"identity": {"account_number": "%s"}}' ${ACCOUNT_NUMBER} | base64)
	if test -z "${CONDUIT_POD}"; then
            CONDUIT_POD=`get_conduit_pod`
	fi
}

check_custom_facts()
{
	if test -f "${CUSTOM_FACTS}"; then
		python -m json.tool ${CUSTOM_FACTS} > /dev/null
	else
		echo "Custom Facts file not found: ${CUSTOM_FACTS}"
		exit 1
	fi
}

if test $# -eq 0; then
	usage
fi

while test $# -gt 0; do
	case "$1" in
	-c|--config|--configuration)
		shift
		CONDUITQE_CONF="$1"
		;;
	-h|--help|help)
		usage
		;;
	auth|identity)
		read_config
		echo "$AUTHENTICATION"
		;;
	register)
		read_config
		sudo subscription-manager config \
			--server.hostname=subscription.rhsm.stage.redhat.com \
			--server.port=443 \
			--server.prefix=/subscription
		sudo subscription-manager orgs \
			--username ${ETHEL_USERNAME} \
			--password ${ETHEL_PASSWORD}
		sudo subscription-manager register \
			--username ${ETHEL_USERNAME} \
			--password ${ETHEL_PASSWORD}
		oc project ${OPENSHIFT_PROJECT}
		oc rsh ${CONDUIT_POD} <<EOF
curl -X POST http://localhost:8080/r/insights/platform/rhsm-conduit/v1/inventories/${ORG_ID}
EOF
		;;
	facts|update-facts)
		read_config
		check_custom_facts
		sudo subscription-manager facts --update
		oc project ${OPENSHIFT_PROJECT}
		oc rsh ${CONDUIT_POD} <<EOF
curl -X POST http://localhost:8080/r/insights/platform/rhsm-conduit/v1/inventories/${ORG_ID}
EOF
		;;
	hosts|inventories)
		read_config
		oc project ${OPENSHIFT_PROJECT} > /dev/null
		oc rsh ${CONDUIT_POD} <<EOF
curl -H "x-rh-identity: ${AUTHENTICATION}" \
	http://insights-inventory.platform-ci.svc:8080/api/inventory/v1/hosts | python -m json.tool
EOF
		;;
	logs|watch-logs)
		read_config
		oc project ${OPENSHIFT_PROJECT}
		oc logs -f ${CONDUIT_POD}
		;;
	pod|conduit-pod)
		read_config
                get_conduit_pod
		;;
	*)
		echo "Unknown option or command: $1"
		usage
		;;
	esac
	shift
done
