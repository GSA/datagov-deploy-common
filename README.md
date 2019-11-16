[![CircleCI](https://circleci.com/gh/GSA/datagov-deploy-common.svg?style=svg)](https://circleci.com/gh/GSA/datagov-deploy-common)

# datagov-deploy-common

Common configuration and baseline for all Data.gov platform nodes.


## Usage

Install the role with a requirements.yml.

```yaml
# requirements.yml
---
- src: https://github.com/GSA/datagov-deploy-common
  version: v1.0.0
  name: gsa.datagov-deploy-common
```

And install with ansible-galaxy.

    $ ansible-galaxy install -r requirements.yml

An example playbook.


```yaml
---
- name: install application
  roles:
    - role: gsa.datagov-deploy-common
```


### Variables

**`common_audit_report_enabled`** boolean (default: false)

Enable or disable the host audit report.


**`common_reboot_notify_email`** string

Email address to send reboot-notify emails.

**`common_operators`** array<object> (default: [])

The list of operators and their public SSH keys to install on the machine for
access.

```
common_operators:
  - username: userone
    email: userone@example.com
    public_key: ssh-rsa aabbccddeeff1234567890 comment
    active: true
```


#### nessus
- `nessus_agent_key`: key used for linking with nessus host (this is a required variable)

- `nessus_agent_group`: host group this agent should be added to when linking with nessus host (this is a required variable)
 
- `nessus_agent_host`: nessus host to link with (default: `cloud.tenable.com`)

- `nessus_agent_port`: nessus host port (default: `443`)

- `nessus_agent_package`: can be either a repository package or a path to a file (default: `NessusAgent`)

        nessus_agent_package: nessus-agent 
        nessus_agent_package: /tmp/nessus-agent_6.8.1_amd64.deb


#### python-upgrade
**`common_python_version_number`** string (default: 2.7.10)

Custom version of python to install.


**`common_python_version_directory`** string (default: `/usr/local/lib/python{{ common_python_version_number }}`)

Directory to install custom python to.


**`common_python_version_url`** string (default: `https://www.python.org/ftp/python/{{ common_python_version_number}}/{{ common_python_version_name }}.tgz`)

URL to download python from.


**`common_python_version_name`** string (default: `Python-{{ common_python_version_number }}`)

Python filename.


### Tags

You can run the playbook with these tags for quicker or targeted plays.


#### audit-report

Configure the audit report.


#### ca-certificates

Install GSA internal CA certificates.


#### filebeat

Filebeat log streaming agent.


#### grub

Grub fixes.


#### hardening

Tasks for OS hardening.


#### hostname

Includes the hostname tasks to update /etc/hosts and hostname.


#### logrotate

Schedule log rotation.


#### nessus

Security compliance scanning agent.


#### newrelic

New Relic host monitoring.


#### ntp

Network Time Protocol agent.


#### postfix

Install and configure postfix mail server for mail relay.


#### python-upgrade

Install a custom version of python.


#### reboot-notify

Send an email to administrators when a reboot is required.


#### system-packages

Install common OS packages.


#### tls

Install the host certificate and key.


#### trendmicro

On-host SecOps managed firewall.


#### unattended-upgrades

Configure unattended-upgrades for automatic apt-get updates/upgrades.


## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for additional information.


## Development

Install dependencies.

    $ pipenv install --dev

Run the playbook with molecule.

    $ pipenv run molecule converge

Run the tests.

    $ pipenv run molecule test

For more information on how to use
[Molecule](https://molecule.readthedocs.io/en/latest/) for development, see [our
wiki](https://github.com/GSA/datagov-deploy/wiki/Developing-Ansible-roles-with-Molecule).


## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in
[CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright
> and related rights in the work worldwide are waived through the [CC0 1.0
> Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication.
> By submitting a pull request, you are agreeing to comply with this waiver of
> copyright interest.
