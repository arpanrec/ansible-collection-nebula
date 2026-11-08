# Ansible Role: Pnpm (arpanrec.nebula.pnpm)

## Pnpm

[pnpm](https://pnpm.io) is a package manager for Node.js projects. The role downloads the standalone Linux release
tarball from the [pnpm GitHub releases](https://github.com/pnpm/pnpm/releases) for the host architecture (`x86_64` or
`aarch64`) and extracts it into the install directory. It then links the `pnpm` executable into the bin path for the
current user. The release does not publish checksums, so the download is not checksum verified. The binary needs no
Node.js installation. The role fails when run as `root`.

The `arpanrec.nebula.nodejs` role does not install pnpm through `npm install -g` or Corepack, so this role is the only
source of `pnpm`.

## Variable

| Variable                      | Type  | Required | Default                                            | Example   | Description                                                                                                                                                                    |
| ----------------------------- | ----- | -------- | -------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `pnpm_rv_install_path`        | `str` | `false`  | `{{ ansible_facts.user_dir }}/.local/share/pnpm`   | -         | Directory the release tarball is extracted into. It is replaced when the installed version differs from the requested one.                                                     |
| `pnpm_rv_executable_bin_path` | `str` | `false`  | `{{ ansible_facts.user_dir }}/.local/bin/pnpm`     | -         | Path of the symlink that points to the `pnpm` executable in the install directory.                                                                                             |
| `pnpm_rv_tmp_download_dir`    | `str` | `false`  | `{{ ansible_facts.user_dir }}/.cache/pnpm-release` | -         | Directory that keeps the downloaded release tarball.                                                                                                                           |
| `pnpm_rv_version`             | `str` | `false`  | `fetch_latest_version`                             | `12.18.0` | Release version, without the `v` prefix. If set to `fetch_latest_version`, it fetches the latest stable release from [GitHub releases](https://github.com/pnpm/pnpm/releases). |

### Example Playbook Pnpm

```yaml
- name: Include Pnpm
  ansible.builtin.import_role:
      name: arpanrec.nebula.pnpm
```

### Testing Pnpm

```bash
molecule test -s role.pnpm.docker
```
