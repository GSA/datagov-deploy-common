import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

operator_key = 'ssh-rsa key operator1@example.com'
inactive_operator_key = 'ssh-rsa key operator_inactive@example.com'


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_ntp_installed(host):
    ntp = host.package('ntp')
    assert ntp.is_installed


def test_ntp_enabled(host):
    ntp = host.service('ntp')

    # For bionic, systemd is not available and this fails
    # assert ntp.is_running

    assert ntp.is_enabled


def test_certificate(host):
    f = host.file('/etc/ssl/certs/datagov_host.crt')

    assert f.exists
    assert f.mode == 0o644
    assert f.user == 'root'
    assert f.group == 'root'


def test_key(host):
    f = host.file('/etc/ssl/private/datagov_host.key')

    assert f.exists
    assert f.mode == 0o640
    assert f.user == 'root'
    assert f.group == 'ssl-cert'


def test_operator_keys(host):
    authorized_keys = host.file('/home/ubuntu/.ssh/authorized_keys')

    assert authorized_keys.contains(operator_key)
    assert not authorized_keys.contains(inactive_operator_key)
