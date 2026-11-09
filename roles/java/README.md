# Ansible Role: Oracle Java (arpanrec.nebula.java)

## Oracle Java

This role installs Oracle JDK, Maven, Gradle, Groovy, Kotlin, and GraalVM in user space. It provides a complete Java development environment with all the necessary tools for Java application development.

**Features:**

- Oracle JDK installation with latest version detection
- Maven build tool for dependency management
- Gradle build automation tool
- Apache Groovy dynamic language
- Kotlin programming language support
- GraalVM high-performance runtime

## Variables

| Variable                           | Type   | Required | Default                                             | Description                                                                                                                                                                                                             |
| ---------------------------------- | ------ | -------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `java_rv_jdk_tmp_dir`              | `str`  | `false`  | `{{ ansible_facts.user_dir }}/.cache/java`          | Temporary directory.                                                                                                                                                                                                    |
| `java_rv_jdk_install_path`         | `str`  | `false`  | `{{ ansible_facts.user_dir }}/.local/share/java`    | Install path for java.                                                                                                                                                                                                  |
| `java_rv_jdk_version`              | `str`  | `false`  | `fetch_latest_version`                              | Example format `21.0.4`. If set to `fetch_latest_version` then the latest version will be installed.                                                                                                                    |
| `java_rv_jdk_mvn_install_path`     | `str`  | `false`  | `{{ ansible_facts.user_dir }}/.local/share/maven`   | Install Path.                                                                                                                                                                                                           |
| `java_rv_jdk_mvn_version`          | `str`  | `false`  | `fetch_latest_version`                              | Exact release version of maven. Example format `maven-3.8.4`. If set to `fetch_latest_version` then the latest version will be installed.                                                                               |
| `java_rv_jdk_gradle_install_path`  | `str`  | `false`  | `{{ ansible_facts.user_dir }}/.local/share/gradle`  | Install path for Gradle.                                                                                                                                                                                                |
| `java_rv_jdk_gradle_version`       | `str`  | `false`  | `fetch_latest_version`                              | Release version of Gradle from [https://gradle.org/releases/](https://gradle.org/releases/). Example format `v7.6.4`. If set to `fetch_latest_version` then the latest version will be installed.                       |
| `java_rv_jdk_groovy_install_path`  | `str`  | `false`  | `{{ ansible_facts.user_dir }}/.local/share/groovy`  | Install path for Groovy.                                                                                                                                                                                                |
| `java_rv_jdk_groovy_version`       | `str`  | `false`  | `fetch_latest_version`                              | Release version of Groovy from [https://groovy.apache.org/download.html](https://groovy.apache.org/download.html). If set to `fetch_latest_version` then the latest version will be installed. Example format `4.0.22`. |
| `java_rv_jdk_kotlinc_install_path` | `str`  | `false`  | `{{ ansible_facts.user_dir }}/.local/share/kotlinc` | Install path for the Kotlin compiler.                                                                                                                                                                                   |
| `java_rv_jdk_kotlinc_version`      | `str`  | `false`  | `fetch_latest_version`                              | Release version of Kotlin. Example format `v2.0.21`. If set to `fetch_latest_version` then the latest version will be installed.                                                                                        |
| `java_rv_jdk_graalvm_install_path` | `str`  | `false`  | `{{ ansible_facts.user_dir }}/.local/share/graalvm` | Install Path for [GraalVM](https://www.graalvm.org/).                                                                                                                                                                   |
| `java_rv_jdk_graalvm_is_install`   | `bool` | `false`  | `false`                                             | Install GraalVM instead of normal JDK.                                                                                                                                                                                  |

## Example Playbook Oracle Java

```yaml
- name: Oracle JDK
  hosts: all
  roles:
      - name: arpanrec.nebula.java
```

## Testing Oracle Java

```bash
molecule test -s role.java.docker
```
