# Ansible Role: Gitleaks (arpanrec.nebula.gitleaks)

## Gitleaks

Gitleaks is a tool for **detecting** secrets like passwords, API keys, and tokens in git repos, files, and whatever else
you wanna throw at it via `stdin`. If you wanna learn more about how the detection engine works check out this
blog: [Regex is (almost) all you need](https://lookingatcomputer.substack.com/p/regex-is-almost-all-you-need).

## Variable

| Variable                          | Type  | Required | Default                                            | Example  | Description                                                                                                                                            |
| --------------------------------- | ----- | -------- | -------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `gitleaks_rv_executable_bin_path` | `str` | `false`  | `{{ ansible_facts.user_dir }}/.local/bin/gitleaks` | -        | Install path for gitleaks.                                                                                                                             |
| `gitleaks_rv_version`             | `str` | `false`  | `fetch_latest_version`                             | `8.28.0` | Release version. If set to `fetch_latest_version`, it will fetch latest release from [Github releases](https://github.com/gitleaks/gitleaks/releases). |
| `gitleaks_rv_tmp_download_dir`    | `str` | `false`  | `{{ ansible_facts.user_dir }}/.cache/gitleaks`     | -        | Cache install directory.                                                                                                                               |

### Example Playbook Gitleaks

```yaml
- name: Include Gitleaks
  ansible.builtin.import_role:
      name: arpanrec.nebula.gitleaks
```

### Testing Gitleaks

```bash
molecule test -s role.gitleaks.docker
```
