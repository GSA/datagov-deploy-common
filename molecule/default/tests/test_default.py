import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

operator_key = 'ssh-rsa key operator1@example.com'
root_key = 'ssh-rsa root_key root@example.com'
inactive_operator_key = 'ssh-rsa key operator_inactive@example.com'


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_audit_report_script(host):
    script = host.file('/usr/local/bin/audit-report.sh')

    assert script.exists
    assert script.user == 'root'
    assert script.group == 'root'
    assert script.mode == 0o755


def test_audit_report_cron(host):
    cron = host.file('/etc/cron.d/audit-report')

    assert cron.exists
    assert cron.user == 'root'
    assert cron.group == 'root'
    assert cron.mode == 0o644

    # Job is disabled by default
    assert cron.contains('^#.*/usr/local/bin/audit-report.sh')


def test_audit_report_ignore(host):
    ignore = host.file('/etc/logwatch/conf/ignore.conf')

    assert ignore.exists
    assert ignore.user == 'root'
    assert ignore.group == 'root'
    assert ignore.mode == 0o644


def test_audit_report_run(host):
    report = host.run('/usr/local/bin/audit-report.sh')

    assert report.succeeded
    assert report.stderr == ''


def test_filebeat_package(host):
    package = host.package("filebeat")

    assert package.is_installed

    major_version = package.version.split('.')[0]
    assert major_version == '6'


def test_filebeat_service(host):
    service = host.service('filebeat')
    assert service.is_running
    assert service.is_enabled


def test_filebeat_config(host):
    config = host.file('/etc/filebeat/filebeat.yml')

    assert config.is_file
    assert config.exists
    assert config.user == 'root'
    assert config.group == 'root'
    assert config.mode == 0o600


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


def test_certificate_symlink(host):
    f = host.file('/usr/local/share/ca-certificates/datagov_host.crt')

    assert f.is_symlink
    assert f.linked_to == '/etc/ssl/certs/datagov_host.crt'
    assert f.user == 'root'


def test_key(host):
    f = host.file('/etc/ssl/private/datagov_host.key')

    assert f.exists
    assert f.mode == 0o640
    assert f.user == 'root'
    assert f.group == 'ssl-cert'


def test_operator_keys(host):
    authorized_keys = host.file('/home/ubuntu/.ssh/authorized_keys')

    assert authorized_keys.contains(operator_key)
    assert authorized_keys.contains(root_key)
    assert not authorized_keys.contains(inactive_operator_key)
