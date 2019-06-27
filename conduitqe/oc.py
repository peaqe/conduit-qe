"""OpenShift CLI (oc) wrapper."""

import logging
import pexpect

OPENSHIFT_URL = 'https://api.insights-dev.openshift.com'

logger = logging.getLogger(__name__)


def oc(params):
    "Run oc with params. May raise 'RuntimeError' on error."
    cmd = f'oc {params}'
    logger.debug(cmd)
    output = pexpect.run(cmd).decode('utf-8')
    if output.startswith('error:') or output.startswith('Error:'):
        raise RuntimeError(output)
    return output


def parse(output):
    "Parse (normalize) output and return a list of lines."
    output = output.split('\r\n')
    output = [line for line in output if line]
    return output


def login(token):
    "Log in with Bearer token."
    cmd = f'login {OPENSHIFT_URL} --token={token}'
    return parse(oc(cmd))


def logout():
    "Log out from OpenShift."
    cmd = 'logout'
    return parse(oc(cmd))


def get_projects():
    "Get all projects."
    cmd = 'projects'
    return parse(oc(cmd))


def get_project():
    "Get current project."
    cmd = 'project'
    return parse(oc(cmd))


def set_project(name):
    "Select project by name."
    cmd = f'project {name}'
    return parse(oc(cmd))


def get_pods():
    "Get all pods."
    cmd = 'get pods'
    return parse(oc(cmd))


def logs(pod):
    "Get logs from pod."
    cmd = f'logs {pod}'
    return parse(oc(cmd))


def exec(pod, command):
    "Execute command in a pod."
    cmd = f'exec {pod} {command}'
    return parse(oc(cmd))


def rsh(pod, command):
    "Open remote shell on pod and execute command in a pod."
    cmd = f'rsh {pod} {command}'
    return parse(oc(cmd))
