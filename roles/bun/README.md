# Ansible Role: Bun (arpanrec.nebula.bun)

## Bun

This role installs [Bun](https://github.com/oven-sh/bun), a JavaScript runtime, bundler, test runner and package
manager. It downloads the release zip, checks it against the release's `SHASUMS256.txt` file, installs the `bun`
executable, and creates a `bunx` symlink to it in the same directory.

## Variable

| Variable                     | Type  | Required | Default                                       | Example | Description                                                                                                                                                                                                 |
| ---------------------------- | ----- | -------- | --------------------------------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bun_rv_executable_bin_path` | `str` | `false`  | `{{ ansible_facts.user_dir }}/.local/bin/bun` | -       | Install path for the `bun` executable. The `bunx` symlink goes in the same directory.                                                                                                                       |
| `bun_rv_version`             | `str` | `false`  | `fetch_latest_version`                        | `1.4.3` | Release version, without the `bun-v` tag prefix. If set to `fetch_latest_version`, it fetches the latest stable release from [Github releases](https://github.com/oven-sh/bun/releases), skipping canaries. |
| `bun_rv_tmp_download_dir`    | `str` | `false`  | `{{ ansible_facts.user_dir }}/.cache/bun`     | -       | Cache install directory.                                                                                                                                                                                    |

### Example Playbook Bun

```yaml
- name: Include Bun
  ansible.builtin.import_role:
      name: arpanrec.nebula.bun
```

### Testing Bun

```bash
molecule test -s role.bun.docker
```
