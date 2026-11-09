# Ansible Role: Terraform (arpanrec.nebula.terraform)

## Terraform

This role installs HashiCorp Terraform infrastructure-as-code tool in user space. It provides automated infrastructure provisioning and management capabilities with latest version detection.

**Features:**

- Terraform CLI installation with latest version detection
- User-space installation (no root privileges required)
- Configurable installation directory
- Automatic version management via HashiCorp releases API
- Support for infrastructure automation and cloud provisioning

Install Terraform in user space

## Variable

| Variable                             | Type  | Required | Default                                         | Example | Description                                                                                                                                                                                             |
| ------------------------------------ | ----- | -------- | ----------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `terraform_rv_install_path`          | `str` | `false`  | `{{ ansible_facts.user_dir }}/.local/bin`       | -       | Install path for terraform.                                                                                                                                                                             |
| `terraform_rv_version`               | `str` | `false`  | `fetch_latest_version`                          | `1.0.9` | Terraform version to install. If set to `fetch_latest_version`, it will fetch the latest release from the api. Get latest release from [releases](https://releases.hashicorp.com/terraform/index.json). |
| `terraform_rv_tmp_install_cache_dir` | `str` | `false`  | `{{ ansible_facts.user_dir }}/.cache/terraform` | -       | Cache install directory.                                                                                                                                                                                |

### Example Playbook Terraform

```yaml
- name: Include Terraform
  ansible.builtin.import_role:
      name: arpanrec.nebula.terraform
```

### Testing Terraform

```bash
molecule test -s role.terraform.docker
```
