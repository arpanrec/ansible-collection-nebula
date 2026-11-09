# Ansible Role: Rclone (arpanrec.nebula.rclone)

## Rclone

This role installs [rclone](https://github.com/rclone/rclone), a command line program to sync files and directories
to and from cloud storage providers. It downloads the release zip, checks it against the release's `SHA256SUMS`
file, and installs the `rclone` executable.

## Variable

| Variable                        | Type  | Required | Default                                          | Example  | Description                                                                                                                                                                 |
| ------------------------------- | ----- | -------- | ------------------------------------------------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rclone_rv_executable_bin_path` | `str` | `false`  | `{{ ansible_facts.user_dir }}/.local/bin/rclone` | -        | Install path for the `rclone` executable.                                                                                                                                   |
| `rclone_rv_version`             | `str` | `false`  | `fetch_latest_version`                           | `1.75.2` | Release version, without the `v` prefix. If set to `fetch_latest_version`, it fetches the latest release from [Github releases](https://github.com/rclone/rclone/releases). |
| `rclone_rv_tmp_download_dir`    | `str` | `false`  | `{{ ansible_facts.user_dir }}/.cache/rclone`     | -        | Cache install directory.                                                                                                                                                    |

### Example Playbook Rclone

```yaml
- name: Include Rclone
  ansible.builtin.import_role:
      name: arpanrec.nebula.rclone
```

### Testing Rclone

```bash
molecule test -s role.rclone.docker
```
