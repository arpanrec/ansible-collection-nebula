# Ansible Role: NodeJS (arpanrec.nebula.nodejs)

## NodeJS

This role installs Node.js runtime environment in user space along with popular global packages. It automatically configures the environment and installs essential development tools.

**Features:**

- Latest Node.js version installation with automatic detection
- Global npm packages, plus pnpm and yarn managed through Corepack
- Essential development tools (Bitwarden CLI, Neovim support, etc.)
- User-space installation (no root privileges required)
- Configurable package list for team consistency

## Variable

| Variable                          | Type   | Required | Default                                                          | Description                                                                                                                                                               |
| --------------------------------- | ------ | -------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `nodejs_rv_install_path`          | `str`  | `false`  | `{{ ansible_facts.user_dir }}/.local/share/node`                 | Install path for nodejs.                                                                                                                                                  |
| `nodejs_rv_version`               | `str`  | `false`  | `fetch_latest_version`                                           | Release version, like `v22.11.0`. If set to `fetch_latest_version`, it will fetch the latest version from the [NodeJS release index](https://nodejs.org/dist/index.json). |
| `nodejs_rv_tmp_install_cache_dir` | `str`  | `false`  | `{{ ansible_facts.user_dir }}/.cache/nodejs`                     | Cache install directory.                                                                                                                                                  |
| `nodejs_rv_global_packages`       | `list` | `false`  | `["@bitwarden/cli", "neovim", "semver", "corepack", "prettier"]` | List of global packages to install.                                                                                                                                       |

### Example Playbook NodeJS

```yaml
- name: Include NodeJS
  ansible.builtin.import_role:
      name: arpanrec.nebula.nodejs
```

### Testing NodeJS

```bash
molecule test -s role.nodejs.docker
```
