#!/usr/bin/python3
"""
Ansible module to recursively set file/directory permissions and ownership.
"""

# Copyright: (c) 2022, Arpan Mandal <me@arpanrec.com>
# MIT (see LICENSE or https://en.wikipedia.org/wiki/MIT_License)

from __future__ import annotations

import dataclasses
import grp
import os
import pwd
import stat
from typing import Any

from ansible.module_utils.basic import AnsibleModule  # type: ignore

DOCUMENTATION = r"""
---
module: arpanrec.nebula.recursive_permissions

short_description: Recursively set file/directory permissions and ownership.

description:
    - Walks one or more directory trees and ensures every file and directory
      has the requested owner, group, and mode.
    - Only changes entries that differ from the desired state, providing
      accurate C(changed) reporting.
    - The root paths themselves are also processed, not just their contents.
    - Symlinks are not followed for traversal. Ownership can be set on symlinks
      via C(lchown), but mode changes are skipped for symlinks (not supported on Linux).

options:
    paths:
        description: List of absolute directory paths to traverse recursively.
        required: true
        type: list
        elements: str
    owner:
        description: Desired owner (username) for all entries.
        required: false
        type: str
    group:
        description: Desired group (group name) for all entries.
        required: false
        type: str
    dir_mode:
        description: Desired octal mode for directories (e.g. C("0750")).
        required: false
        type: str
    file_mode:
        description: Desired octal mode for regular files (e.g. C("0640")).
        required: false
        type: str

author:
    - Arpan Mandal (mailto:me@arpanrec.com)
"""

EXAMPLES = r"""
---
- name: Jellyfin | Container | Fix Permissions On Jellyfin Directories
  arpanrec.nebula.recursive_permissions:
      paths:
          - /app/jellyfin-container-root
          - /app/jellyfin-media
      owner: jellyfin
      group: jellyfin
      dir_mode: "0750"
      file_mode: "0640"

- name: Fix Only Ownership Without Changing Modes
  arpanrec.nebula.recursive_permissions:
      paths:
          - /srv/data
      owner: appuser
      group: appgroup
"""

RETURN = r"""
---
total_changed:
    description: Total number of files and directories that were changed (or would be changed in check mode).
    type: int
    returned: always
changes:
    description: >-
        List of changes made (or that would be made in check mode).
        Each entry is a dict with the path and the before/after values for any attribute that differed.
    type: list
    elements: dict
    returned: always
    sample:
        - path: "/srv/jellyfin/config/settings.json"
          from_mode: "0644"
          to_mode: "0640"
          from_owner: 0
          to_owner: 1001
          from_group: 0
          to_group: 1001
"""


@dataclasses.dataclass
class _DesiredState:
    """Desired ownership and mode to reconcile every entry towards."""

    uid: int | None = None
    gid: int | None = None
    dir_mode: int | None = None
    file_mode: int | None = None


# pylint: disable=too-few-public-methods
class RecursivePermissions:
    """Reconcile file/directory permissions and ownership across directory trees."""

    def __init__(self, module: AnsibleModule) -> None:
        self.module = module
        self.check_mode: bool = module.check_mode
        self.changed: bool = False
        self.changes: list[dict[str, Any]] = []

        self.paths: list[str] = module.params["paths"]

        owner: str | None = module.params["owner"]
        group: str | None = module.params["group"]
        dir_mode_str: str | None = module.params["dir_mode"]
        file_mode_str: str | None = module.params["file_mode"]

        self.desired = _DesiredState()

        if owner is not None:
            try:
                self.desired.uid = pwd.getpwnam(owner).pw_uid
            except KeyError as exc:
                raise ValueError(f"owner '{owner}' does not exist") from exc

        if group is not None:
            try:
                self.desired.gid = grp.getgrnam(group).gr_gid
            except KeyError as exc:
                raise ValueError(f"group '{group}' does not exist") from exc

        if dir_mode_str is not None:
            self.desired.dir_mode = int(dir_mode_str, 8)

        if file_mode_str is not None:
            self.desired.file_mode = int(file_mode_str, 8)

    def _process_entry(self, path: str, is_dir: bool) -> None:
        try:
            st = os.lstat(path)
        except FileNotFoundError:
            return

        is_symlink = stat.S_ISLNK(st.st_mode)
        current_mode = stat.S_IMODE(st.st_mode)
        desired_mode = self.desired.dir_mode if is_dir else self.desired.file_mode

        mode_changed = desired_mode is not None and current_mode != desired_mode and not is_symlink
        owner_changed = self.desired.uid is not None and st.st_uid != self.desired.uid
        group_changed = self.desired.gid is not None and st.st_gid != self.desired.gid

        if not (mode_changed or owner_changed or group_changed):
            return

        self.changed = True
        change: dict[str, Any] = {"path": path}
        if mode_changed:
            change["from_mode"] = format(current_mode, "04o")
            change["to_mode"] = format(desired_mode, "04o")  # type: ignore[arg-type]
        if owner_changed:
            change["from_owner"] = st.st_uid
            change["to_owner"] = self.desired.uid
        if group_changed:
            change["from_group"] = st.st_gid
            change["to_group"] = self.desired.gid
        self.changes.append(change)

        if self.check_mode:
            return

        if mode_changed:
            os.chmod(path, desired_mode)  # type: ignore[arg-type]
        if owner_changed or group_changed:
            uid_to_set = self.desired.uid if owner_changed else -1
            gid_to_set = self.desired.gid if group_changed else -1
            os.lchown(path, uid_to_set, gid_to_set)  # type: ignore[arg-type]

    def _process_tree(self, root_path: str) -> None:
        if not os.path.exists(root_path):
            self.module.fail_json(  # pyright: ignore[reportUnknownMemberType]
                msg=f"Path does not exist: {root_path}", changed=self.changed
            )

        self._process_entry(root_path, is_dir=True)

        for dirpath, dirnames, filenames in os.walk(root_path, followlinks=False):
            for dirname in dirnames:
                self._process_entry(os.path.join(dirpath, dirname), is_dir=True)
            for filename in filenames:
                self._process_entry(os.path.join(dirpath, filename), is_dir=False)

    def reconcile(self) -> dict[str, Any]:
        """Bring all paths into the desired state and return the module result."""
        for path in self.paths:
            self._process_tree(path)
        return {
            "changed": self.changed,
            "total_changed": len(self.changes),
            "changes": self.changes,
        }


def run_module() -> None:
    """Ansible entry point."""
    module_args: dict[str, Any] = {
        "paths": {"type": "list", "elements": "str", "required": True},
        "owner": {"type": "str", "required": False, "default": None},
        "group": {"type": "str", "required": False, "default": None},
        "dir_mode": {"type": "str", "required": False, "default": None},
        "file_mode": {"type": "str", "required": False, "default": None},
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_one_of=[["owner", "group", "dir_mode", "file_mode"]],
    )

    try:
        result = RecursivePermissions(module).reconcile()
        module.exit_json(**result)  # type: ignore
    except (OSError, ValueError) as exc:
        module.fail_json(msg=f"Failed to set recursive permissions: {exc}", changed=False)  # type: ignore


def main() -> None:
    """Python main module."""
    run_module()


if __name__ == "__main__":
    main()
