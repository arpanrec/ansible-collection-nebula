# Ansible Role: Bitwarden Secrets Manager SDK (arpanrec.nebula.bws)

## Bitwarden Secrets Manager SDK

This role installs the Bitwarden Secrets Manager SDK CLI tool for automated secrets management. It provides secure access to Bitwarden secrets for CI/CD pipelines and server automation.

**Features:**

- BWS SDK CLI installation with latest version detection
- Secure secrets management for automation workflows
- Integration with Bitwarden Secrets Manager
- User-space installation with configurable paths
- Automatic GitHub API version detection
- Support for CI/CD and server automation use cases

Install [Bitwarden Secrets Manager SDK](https://bitwarden.com/help/secrets-manager-sdk/)

Variables:

| Variable              | Type  | Required | Default                                       | Example      | Description                                                                                                                                                                                                                                                                                                                                                             |
| --------------------- | ----- | -------- | --------------------------------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bws_sdk_version_tag` | `str` | `false`  | `fetch_latest_version`                        | `bws-v1.0.0` | Version of [Bitwarden BWS SDK ClI](https://github.com/bitwarden/sdk-sm/releases). Like [bws-v1.0.0](https://github.com/bitwarden/sdk-sm/releases/tag/bws-v1.0.0). Default Get latest release name from [github](https://api.github.com/repos/bitwarden/sdk-sm/releases/latest). If set to `fetch_latest_version`, it will fetch the latest release from the github api. |
| `bws_sdk_bin_dir`     | `str` | `false`  | `{{ ansible_facts.user_dir }}/.local/bin`     | -            | Directory to install BWS                                                                                                                                                                                                                                                                                                                                                |
| `bws_sdk_tmp_dir`     | `str` | `false`  | `{{ ansible_facts.user_dir }}/.cache/bws_sdk` | -            | Directory to temporary download BWS.                                                                                                                                                                                                                                                                                                                                    |

### Example Playbook Bitwarden Secrets Manager SDK

```yaml
- name: Include Bitwarden Secrets Manager SDK
  ansible.builtin.import_role:
      name: arpanrec.nebula.bws
```

### Testing Bitwarden Secrets Manager SDK

```bash
molecule test -s role.bws.docker
```
