# Ansible Collection Nebula (arpanrec.nebula)

## Description

This collection provides a set of roles to deploy and manage various services.

## Roles

- [Bitwarden Secrets Manager CLI (bws)](/roles/bws/README.md)
- [The Go Programming Language (go)](/roles/go/README.md)
- [Oracle Java (java)](/roles/java/README.md)
- [Linux Patching (linux_patching)](/roles/linux_patching/README.md)
- [NodeJS (nodejs)](/roles/nodejs/README.md)
- [SSH Hardening (ssh_hardening)](/roles/ssh_hardening/README.md)
- [Terraform by HashiCorp (terraform)](/roles/terraform/README.md)
- [User Add (user_add)](/roles/user_add/README.md)
- [Vault by HashiCorp (vault)](/roles/vault/README.md)
- [Pulumi (pulumi)](/roles/pulumi/README.md)
- [Gitea (gitea)](/roles/gitea/README.md)
- [PostgreSQL (postgresql)](/roles/postgresql/README.md)
- [Hadolint (hadolint)](/roles/hadolint/README.md)
- [Gitleaks (gitleaks)](/roles/gitleaks/README.md)
- [Uv (uv)](/roles/uv/README.md)
- [Rclone (rclone)](/roles/rclone/README.md)

## Playbooks

- [server_workspace](/playbooks/server_workspace.md)
- [cloudinit](/playbooks/cloudinit.md)

## Plugins

### Modules

- [recursive_permissions](/plugins/modules/recursive_permissions.py)

### Lookups

- [bitwarden](/plugins/lookup/bitwarden.py)
- [version_db](/plugins/lookup/version_db.py)

### Filters

- [san_list_transformer](/plugins/filter/san_list_transformer.py)
- [split_certificates](/plugins/filter/split_certificates.py)

## Installation

```bash
export NEBULA_VERSION=1.20.0
curl "https://raw.githubusercontent.com/arpanrec/ansible-collection-nebula/refs/tags/${NEBULA_VERSION}/requirements.yml" \
    -o "/tmp/requirements-${NEBULA_VERSION}.yml"
ansible-galaxy install -r "/tmp/requirements-${NEBULA_VERSION}.yml"
ansible-galaxy collection install "git+https://github.com/arpanrec/ansible-collection-nebula.git,${NEBULA_VERSION}"
```

## [License](LICENSE)

`MIT`
