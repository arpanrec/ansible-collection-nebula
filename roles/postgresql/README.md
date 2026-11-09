# Ansible Role: postgresql (arpanrec.nebula.postgresql)

## Postgresql

This role installs a postgresql server managed by systemd and pg_ctlcluster.

## Variables

| Variable                          | Type  | Required | Default | Description                       |
| --------------------------------- | ----- | -------- | ------- | --------------------------------- |
| `postgresql_version`              | `str` | `false`  | `18`    | Postgresql major version.         |
| `postgresql_cluster`              | `str` | `false`  | `main`  | Postgres cluster name.            |
| `postgresql_port`                 | `int` | `false`  | `5432`  | Postgresql port.                  |
| `postgresql_super_user_password`  | `str` | `false`  | None    | Root user password.               |
| `postgresql_ssl_cert_pem_content` | `str` | `false`  | None    | DB SSL Certificate pem content.   |
| `postgresql_ssl_key_pem_content`  | `str` | `false`  | None    | DB SSL Key pem content.           |
| `postgresql_ssl_ca_pem_content`   | `str` | `false`  | None    | Root certificate for Client Auth. |

### postgresql_extra_hba_rules

Extra rules to add to the `pg_hba.conf` file.
Default rules are in [var file](vars/main.yml), var: [postgresql_hba_rules](vars/main.yml#postgresql_hba_rules) file and can cause a conflict with your own.

```yaml
postgresql_extra_hba_rules:
    - contype: # Conn type local, hostssl, host
      databases: # DB Name
      users: # user name
      method: # Auth method, md5, peer, scram-sha-256, cert
      options: # Extra auth option like: clientcert=verify-full / clientcert=verify-ca
```

### postgresql_extra_conf_options

Extra rules to add to the `postgresql.conf` file.
Default rules are in [var file](vars/main.yml), var: [postgresql_conf_options](vars/main.yml#postgresql_conf_options) file and can cause a conflict with your own.

```yaml
postgresql_extra_conf_options:
    - option: # Name of the key
      value: # Option value, make sure to wrap complex vars in single quote like "'{{ extra_option_value }}'"
```

### postgresql_users

Users to ensure exist.

```yaml
postgresql_users:
    - name: jdoe #required; the rest are optional
      password: # defaults to not set
      encrypted: # defaults to not set
      role_attr_flags: # defaults to not set
      login_db: # defaults to postgresql_super_user_db
      login_host: # defaults to 'localhost'
      login_password: # defaults to not set
      login_user: # defaults to '{{ postgresql_super_user }}'
      login_unix_socket: # defaults to 1st of postgresql_unix_socket_directories
      login_port: # defaults to postgresql_port
      state: # defaults to 'present'
```

### postgresql_databases

Databases to ensure exist.

```yaml
postgresql_databases:
    - name: exampledb # required; the rest are optional
      lc_collate: # defaults to 'en_US.UTF-8'
      lc_ctype: # defaults to 'en_US.UTF-8'
      encoding: # defaults to 'UTF-8'
      template: # defaults to 'template0'
      login_host: # defaults to 'localhost'
      login_password: # defaults to not set
      login_user: # defaults to '{{ postgresql_super_user }}'
      login_unix_socket: # defaults to 1st of postgresql_unix_socket_directories
      login_port: # defaults to postgresql_port
      owner: # defaults to postgresql_super_user
      state: # defaults to 'present'
```

### postgresql_privs

[Privileges to configure](https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_privs_module.html#ansible-collections-community-postgresql-postgresql-privs-module)

```yaml
postgresql_privs:
    - login_db: exampledb # database (required)
      roles: jdoe # role(s) the privs apply to (required)
      privs: # comma separated list of privileges - defaults to not set
      type: # type of database object to set privileges on - defaults to not set
      objs: # list of database objects to set privileges on - defaults to not set
      schema: # defaults to not set
      session_role: # defaults to not set
      fail_on_role: # defaults to true
      grant_option: # defaults to not set
      target_roles: # defaults to not set
      login_host: # defaults to 'localhost'
      login_password: # defaults to not set
      login_user: # defaults to '{{ postgresql_super_user }}'
      login_unix_socket: # defaults to 1st of postgresql_unix_socket_directories
      login_port: # defaults to postgresql_port
      state: # defaults to 'present'
```

### Example Playbook postgresql

```yaml
- name: Include postgresql
  ansible.builtin.import_role:
      name: arpanrec.nebula.postgresql
```
