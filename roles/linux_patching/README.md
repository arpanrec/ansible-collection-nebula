# Ansible Role Linux Patching (arpanrec.nebula.linux_patching)

This role provides comprehensive system configuration and package management for Debian-based systems. It installs essential packages, development tools, and configures system settings for optimal server and development environments.

**Features:**

- System package installation and updates for Debian-based distributions
- Essential development tools and utilities installation
- System configuration (timezone, locale, hostname, domain)
- Security hardening with firewall (ufw) and access controls
- Root CA certificate management for organization PKI
- SSH configuration and networking setup
- Configurable package lists for different use cases (base system vs. development)

Install all the latest packages on Debian-based systems.
Also Install basic utility tools for server.
Set timezone, locale, and loopback ip in server

## Role Variables

| Variable                                   | Type        | Required | Default                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Description                                            |
| ------------------------------------------ | ----------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| `linux_patching_rv_packages`               | `list[str]` | `false`  | `["ca-certificates", "sudo", "systemd", "apt-transport-https", "locales", "systemd-timesyncd", "network-manager", "gnupg2", "gnupg", "acl", "ufw", "procps", "apt-utils", "lsb-release", "python3", "openssl", "util-linux-extra", "nftables", "libatomic1"]`                                                                                                                                                                                              | Install the packages in the distributions.             |
| `linux_patching_rv_devel_packages`         | `list[str]` | `false`  | `["net-tools", "telnet", "vim", "git", "git-lfs", "jq", "zsh", "htop", "tmux", "tree", "luarocks", "build-essential", "ninja-build", "gettext", "cmake", "make", "openssh-client", "rsync", "ntfs-3g", "exfat-fuse", "python3-pip", "python3-venv", "python3-dev", "zip", "unzip", "tar", "wget", "curl", "pigz", "xz-utils", "gzip", "bzip2", "autoconf", "automake", "gcc", "g++", "clang", "libglib2.0-dev", "libssl-dev", "libffi-dev", "zlib1g-dev"]` | Install the development packages in the distributions. |
| `linux_patching_rv_install_devel_packages` | `bool`      | `false`  | `true`                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Install the development packages in the distributions. |
| `linux_patching_rv_extra_packages`         | `list[str]` | `false`  | -                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Install extra required the packages.                   |
| `linux_patching_rv_timezone`               | `str`       | `false`  | `Asia/Kolkata`                                                                                                                                                                                                                                                                                                                                                                                                                                             | Set the ZoneTime info in server.                       |
| `linux_patching_rv_hostname`               | `str`       | `false`  | `localhost` or `{{ ansible_facts.hostname }}`                                                                                                                                                                                                                                                                                                                                                                                                              | Cluster / Public Host name. (Doesn't work with docker) |
| `linux_patching_rv_domain_name`            | `str`       | `false`  | `{{ ansible_facts.domain }}`                                                                                                                                                                                                                                                                                                                                                                                                                               | Domain Name                                            |
| `linux_patching_rv_root_ca_pem_content`    | `str`       | `false`  | -                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Organization Root CA certificate.                      |
| `linux_patching_rv_ssh_port`               | `int`       | `false`  | `22`                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Default SSH Port                                       |

## Example Playbook

```yaml
---
- name: Patch Debian System
  ansible.builtin.import_role:
      name: arpanrec.nebula.linux_patching
```

## Testing

```bash
molecule test -s role.linux_patching.default
```
