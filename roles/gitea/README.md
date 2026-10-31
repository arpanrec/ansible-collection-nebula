# Ansible Role: Gitea (arpanrec.nebula.gitea)

## Gitea

This role installs a Gitea managed by systemd.

## Variables

| Variable                                           | Type  | Required | Default                                                                                                    | Description                                                                                                                                  |
| -------------------------------------------------- | ----- | -------- | ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `gitea_cluster_name`                               | `str` | `false`  | `main`                                                                                                     | Isolated gitea instance.                                                                                                                     |
| `gitea_working_directory`                          | `str` | `false`  | `/var/lib/gitea/{{ gitea_cluster_name }}`                                                                  | Gitea Data directory.                                                                                                                        |
| `gitea_service_group`                              | `str` | `false`  | `gitea-{{ gitea_cluster_name }}`                                                                           | Gitea Service Group.                                                                                                                         |
| `gitea_service_user`                               | `str` | `false`  | `{{ gitea_service_group }}`                                                                                | Gitea Service User.                                                                                                                          |
| `gitea_service_user_home_directory`                | `str` | `false`  | `{{ gitea_working_directory }}`                                                                            | Gitea Service User Home Directory.                                                                                                           |
| `gitea_rv_version`                                 | `str` | `false`  | `fetch_latest_version`                                                                                     | If set to `fetch_latest_version` it will pull from [Gitea version](https://github.com/go-gitea/gitea/releases), else something like `1.24.6` |
| `gitea_http_port`                                  | `int` | `false`  | `8582`                                                                                                     | Http port.                                                                                                                                   |
| `gitea_ssh_port`                                   | `int` | `false`  | `8583`                                                                                                     | SSH port.                                                                                                                                    |
| `gitea_domain`                                     | `str` | `false`  | `{{ ansible_facts.fqdn }}`                                                                                 | Gitea communication URL.                                                                                                                     |
| `gitea_ssh_domain`                                 | `str` | `false`  | `{{ gitea_domain }}`                                                                                       | Gitea SSH URL.                                                                                                                               |
| `gitea_protocol`                                   | `str` | `false`  | `https` when both `gitea_http_cert_pem_content` and `gitea_http_key_pem_content` are set, otherwise `http` | URL scheme used in `gitea_local_root_url`.                                                                                                   |
| `gitea_local_root_url`                             | `str` | `false`  | `{{ gitea_protocol }}://{{ gitea_domain }}:{{ gitea_http_port }}`                                          | Local (DMZ) URL for Gitea workers (such as SSH update) accessing web service.                                                                |
| `gitea_root_url`                                   | `str` | `false`  | `{{ gitea_local_root_url }}`                                                                               | This is useful if the internal and the external URL don't match (e.g. behind a reverse proxy).                                               |
| `gitea_ssh_server_user`                            | `str` | `false`  | `{{ gitea_service_user }}`                                                                                 | Username to use for the built-in SSH Server.                                                                                                 |
| `gitea_http_cert_pem_content`                      | `str` | `false`  | None                                                                                                       | Gitea SSL Certificate pem content.                                                                                                           |
| `gitea_http_key_pem_content`                       | `str` | `false`  | None                                                                                                       | Gitea SSL Key pem content.                                                                                                                   |
| `gitea_secret_key`                                 | `str` | `false`  | None                                                                                                       | Global secret key (Generated automatically if not provided).                                                                                 |
| `gitea_internal_token`                             | `str` | `false`  | None                                                                                                       | Internal secret within Gitea binary (generated automatically if not provided).                                                               |
| `gitea_oauth2_jwt_secret`                          | `str` | `false`  | None                                                                                                       | OAuth2 authentication secret (generated automatically if not provided).                                                                      |
| `gitea_lfs_jwt_secret`                             | `str` | `false`  | None                                                                                                       | LFS authentication secret (generated automatically if not provided).                                                                         |
| `gitea_admin_user_username`                        | `str` | `false`  | None                                                                                                       | Gitea admin user username.                                                                                                                   |
| `gitea_admin_user_password`                        | `str` | `false`  | None                                                                                                       | Gitea admin user password.                                                                                                                   |
| `gitea_admin_user_email`                           | `str` | `false`  | None                                                                                                       | Gitea admin user email address.                                                                                                              |
| `gitea_global_runner_registration_token_file_path` | `str` | `false`  | None                                                                                                       | Writes the global runner token to this file.                                                                                                 |
| `gitea_admin_token_file_path`                      | `str` | `false`  | None                                                                                                       | Writes the admin user token to file.                                                                                                         |

### gitea_config_db_postgresql

[Postgres database configuration](https://docs.gitea.com/administration/config-cheat-sheet#database-database).

```yaml
---
gitea_config_db_postgresql:
    host: '127.0.0.1:5432'
    name: 'gitea'
    user: 'root'
    passwd: 'password'
    schema: 'public'
    ssl_mode: 'disable' # ["disable", "require", "verify-ca", "verify-full"]
    pg_ssl_root_cert_pem_content: '' # Pem content of root certificate.
    pg_ssl_client_cert_pem_content: '' # Pem content of the certificate or full chain.
    pg_ssl_client_key_pem_content: '' # Pem content of the private key.
```

postgresql ssl config files are written to

```yaml
gitea_config_db_pg_ssl_root_cert_file: '{{ gitea_service_user_home_directory }}/.postgresql/root.crt'
gitea_config_db_pg_ssl_cert_file: '{{ gitea_service_user_home_directory }}/.postgresql/postgresql.crt'
gitea_config_db_pg_ssl_key_file: '{{ gitea_service_user_home_directory }}/.postgresql/postgresql.key'
```

### gitea_extra_config

[Gitea extra configuration](https://docs.gitea.com/administration/config-cheat-sheet).

```yaml
gitea_extra_config:
    - section: ''
      option: ''
      value: ''
```

## Backup

```yaml
gitea_working_directory: '/var/lib/gitea/{{ gitea_cluster_name }}'
gitea_service_user_home_directory: '{{ gitea_working_directory }}'
```

For backup just backup the `gitea_working_directory` if nothing else is configured.

### Example Playbook gitea

```yaml
- name: Include Gitea
  ansible.builtin.import_role:
      name: arpanrec.nebula.gitea
```

Just write the admin token to file.

```yaml
- name: Gitea | Admin token temp file.
  ansible.builtin.tempfile:
      state: file
      suffix: .txt
  register: __gitea_admin_token_file

- name: Gitea | Write admin token.
  ansible.builtin.import_role:
      name: arpanrec.nebula.gitea
      tasks_from: admin-token.yml
  vars:
      gitea_admin_token_file_path: '{{ __gitea_admin_token_file.path }}'
      gitea_admin_user_username: 'admin-user'
```
