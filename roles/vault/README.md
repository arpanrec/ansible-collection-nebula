# Ansible Role: Vault (arpanrec.nebula.vault)

## Hashicorp Vault

This role installs HashiCorp Vault secrets management platform in user space. Vault provides secure storage and access to secrets, encryption keys, and sensitive data for modern applications.

**Features:**

- Vault CLI installation with latest version detection
- User-space installation (no root privileges required)
- Secure secrets management and encryption services
- Integration with cloud platforms and Kubernetes
- Configurable installation directory
- Automatic version management via HashiCorp releases API

Install Hashicorp Vault in user space

## Variable

| Variable                         | Type  | Required | Default                                     | Example  | Description                                                                                                                                                                                  |
| -------------------------------- | ----- | -------- | ------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `vault_rv_install_path`          | `str` | `false`  | `{{ ansible_facts.user_dir }}/.local/bin`   | -        | Install path for vault.                                                                                                                                                                      |
| `vault_rv_version`               | `str` | `false`  | `fetch_latest_version`                      | `1.16.2` | Vault Release version. If set to `fetch_latest_version`, it will fetch the latest release from the api. Get latest release from [releases](https://releases.hashicorp.com/vault/index.json). |
| `vault_rv_tmp_install_cache_dir` | `str` | `false`  | `{{ ansible_facts.user_dir }}/.cache/vault` | -        | Cache install directory.                                                                                                                                                                     |

### Example Playbook Vault

```yaml
- name: Include Vault
  ansible.builtin.import_role:
      name: arpanrec.nebula.vault
```

### Testing Vault

```bash
molecule test -s role.vault.docker
```
