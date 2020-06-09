import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

operator_key = 'ssh-rsa key operator1@example.com'
inactive_operator_key = 'ssh-rsa key operator_inactive@example.com'


def test_ua_package(host):
    package = host.package("ubuntu-advantage-tools")

    assert package.is_installed
