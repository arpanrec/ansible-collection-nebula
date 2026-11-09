# Security Policy

## Supported versions

| Version                              | Supported          |
| ------------------------------------ | ------------------ |
| Latest 1.x release on Ansible Galaxy | :white_check_mark: |
| `main` branch                        | :white_check_mark: |
| Older 1.x releases                   | :x:                |

Security fixes go into the `main` branch and ship in the next release. If you run an older version, upgrade before reporting.

## Reporting a vulnerability

Do not open a public issue, discussion, or pull request for a security problem.

Report it privately through GitHub: go to the [Security tab](https://github.com/arpanrec/ansible-collection-nebula/security) and click **Report a vulnerability**, or open the [advisory form](https://github.com/arpanrec/ansible-collection-nebula/security/advisories/new) directly.

Include as much of the following as you can:

- The affected collection version or commit
- The role, plugin, or playbook involved, and the target OS and Ansible version
- Steps to reproduce, with a minimal playbook and inventory (remove real secrets, tokens, and hostnames)
- What an attacker can do with the issue

The report stays private between you and the maintainers until a fix is released. Once it ships, the advisory is published and you are credited unless you ask not to be.

## Scope

In scope are the roles, plugins, and playbooks in this collection, for example a role that leaves files with loose permissions, writes secrets to logs, or installs a binary without verifying it.

Vulnerabilities in the software these roles install (Vault, Gitea, PostgreSQL, Node.js, and so on) belong with those projects. The vendored `geerlingguy.docker` role belongs with its upstream project unless the issue comes from changes made here.
