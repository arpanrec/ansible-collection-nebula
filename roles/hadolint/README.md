# Ansible Role: Hadolint (arpanrec.nebula.hadolint)

## Hadolint

This role installs Hadolint. A smarter Dockerfile linter that helps you build best practice Docker images. The linter
parses the Dockerfile into an AST and performs rules on top of the AST. It stands on the shoulders of ShellCheck to lint
the Bash code inside RUN instructions.

## Variable

| Variable                            | Type  | Required | Default                                            | Example   | Description                                                                                                                                            |
| ----------------------------------- | ----- | -------- | -------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `hadolint_rv_executable_bin_path`   | `str` | `false`  | `{{ ansible_facts.user_dir }}/.local/bin/hadolint` | -         | Install path for hadolint.                                                                                                                             |
| `hadolint_rv_version`               | `str` | `false`  | `fetch_latest_version`                             | `v2.13.1` | Release version. If set to `fetch_latest_version`, it will fetch latest release from [Github releases](https://github.com/hadolint/hadolint/releases). |
| `hadolint_rv_tmp_install_cache_dir` | `str` | `false`  | `{{ ansible_facts.user_dir }}/.cache/hadolint`     | -         | Cache install directory.                                                                                                                               |

### Example Playbook Hadolint

```yaml
- name: Include Hadolint
  ansible.builtin.import_role:
      name: arpanrec.nebula.hadolint
```

### Testing Hadolint

```bash
molecule test -s role.hadolint.docker
```
