# Ansible Role: Pulumi (arpanrec.nebula.pulumi)

## Pulumi

This role installs Pulumi infrastructure-as-code platform in user space. Pulumi allows you to create, deploy, and manage cloud infrastructure using familiar programming languages.

**Features:**

- Pulumi CLI installation with latest version detection from GitHub
- User-space installation (no root privileges required)
- Support for multiple programming languages (TypeScript, Python, Go, C#, Java)
- Cloud-agnostic infrastructure provisioning
- Configurable installation and cache directories
- Integration with modern development workflows

Install [Pulumi](https://github.com/pulumi/pulumi) in user space.

## Variable

| Variable                          | Type  | Required | Default                                      | Example    | Description                                                                                                                                                         |
| --------------------------------- | ----- | -------- | -------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pulumi_rv_install_path`          | `str` | `false`  | `{{ ansible_facts.user_dir }}/.pulumi/bin`   | -          | Install path for pulumi.                                                                                                                                            |
| `pulumi_rv_version`               | `str` | `false`  | `fetch_latest_version`                       | `v3.116.0` | Release version. If set to `fetch_latest_version`, it will fetch latest release from [Github releases](https://api.github.com/repos/pulumi/pulumi/releases/latest). |
| `pulumi_rv_tmp_install_cache_dir` | `str` | `false`  | `{{ ansible_facts.user_dir }}/.cache/pulumi` | -          | Cache install directory.                                                                                                                                            |

### Example Playbook Pulumi

```yaml
- name: Include Pulumi
  ansible.builtin.import_role:
      name: arpanrec.nebula.pulumi
```

### Testing Pulumi

```bash
molecule test -s role.pulumi.docker
```
