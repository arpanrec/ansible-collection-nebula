# Ansible Role: Uv (arpanrec.nebula.uv)

## Uv

This role installs [uv](https://github.com/astral-sh/uv), an extremely fast Python package and project manager,
written in Rust. It installs both the `uv` and `uvx` executables.

## Variable

| Variable                    | Type  | Required | Default                                      | Example | Description                                                                                                                                       |
| --------------------------- | ----- | -------- | -------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `uv_rv_executable_bin_path` | `str` | `false`  | `{{ ansible_facts.user_dir }}/.local/bin/uv` | -       | Install path for the `uv` executable. `uvx` is installed alongside it in the same directory.                                                      |
| `uv_rv_version`             | `str` | `false`  | `fetch_latest_version`                       | `0.9.7` | Release version. If set to `fetch_latest_version`, it will fetch latest release from [Github releases](https://github.com/astral-sh/uv/releases). |
| `uv_rv_tmp_download_dir`    | `str` | `false`  | `{{ ansible_facts.user_dir }}/.cache/uv`     | -       | Cache install directory.                                                                                                                          |

### Example Playbook Uv

```yaml
- name: Include Uv
  ansible.builtin.import_role:
      name: arpanrec.nebula.uv
```

### Testing Uv

```bash
molecule test -s role.uv.docker
```
