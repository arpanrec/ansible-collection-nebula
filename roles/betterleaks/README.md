# Ansible Role: Betterleaks (arpanrec.nebula.betterleaks)

## Betterleaks

[Betterleaks](https://github.com/betterleaks/betterleaks) scans git repositories, files, and `stdin` for secrets such
as passwords, API keys, and tokens. The role downloads the Linux release tarball for the host architecture (`x86_64`
or `aarch64`), verifies it against the release's `checksums.txt`, and keeps it in the download cache directory. It then
extracts only the `betterleaks` binary into a temporary directory, copies it to the install path for the current user,
and removes the temporary directory. The role fails when run as `root`.

## Variable

| Variable                             | Type  | Required | Default                                               | Example | Description                                                                                                                                                                                  |
| ------------------------------------ | ----- | -------- | ----------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `betterleaks_rv_executable_bin_path` | `str` | `false`  | `{{ ansible_facts.user_dir }}/.local/bin/betterleaks` | -       | Install path for betterleaks.                                                                                                                                                                |
| `betterleaks_rv_version`             | `str` | `false`  | `fetch_latest_version`                                | `1.9.0` | Release version, without the `v` prefix. If set to `fetch_latest_version`, it fetches the latest stable release from [GitHub releases](https://github.com/betterleaks/betterleaks/releases). |
| `betterleaks_rv_tmp_download_dir`    | `str` | `false`  | `{{ ansible_facts.user_dir }}/.cache/betterleaks`     | -       | Directory that keeps the downloaded release tarball.                                                                                                                                         |

### Example Playbook Betterleaks

```yaml
- name: Include Betterleaks
  ansible.builtin.import_role:
      name: arpanrec.nebula.betterleaks
```

### Testing Betterleaks

```bash
molecule test -s role.betterleaks.docker
```
