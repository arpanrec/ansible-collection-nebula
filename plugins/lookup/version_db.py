#!/usr/bin/python3
"""
Ansible Module for Search for the latest release in a GitHub repository.
"""

from __future__ import annotations

import json
from typing import Any

from ansible.errors import AnsibleLookupError  # type: ignore
from ansible.plugins.lookup import LookupBase  # type: ignore
from ansible.utils.display import Display  # type: ignore

# pylint: disable=import-error,no-name-in-module
from ansible_collections.arpanrec.nebula.plugins.module_utils.version_db import get_version  # type: ignore
from ansible_collections.arpanrec.nebula.plugins.module_utils.version_db.models import VersionDetails  # type: ignore

DOCUMENTATION = """
---
name: version_db
author:
    - Arpan Mandal <me@arpanrec.com>
short_description: Get download and version details for a supported application.
description:
    - Resolve the version, download link, checksum and any extra details for a supported application.
    - One of V(bws), V(terraform), V(vault), V(go), V(java), V(nodejs), V(pulumi), V(gitea),
      V(hadolint), V(gitleaks), V(uv) or V(rclone) must be supplied as the single term.
    - The result is returned as a one-element list containing a JSON encoded object.
notes:
    - This lookup reads C(ansible_architecture) from the host variables to build architecture
      specific download links, so C(gather_facts) must be enabled (or the fact otherwise provided).
options:
    _terms:
        description: The application name to resolve version details for.
        required: true
        type: str
"""

EXAMPLES = """
---
- name: Resolve the latest Terraform version details
  ansible.builtin.debug:
      msg: "{{ lookup('arpanrec.nebula.version_db', 'terraform') | from_json }}"

- name: Resolve a pinned Vault version
  ansible.builtin.debug:
      msg: "{{ lookup('arpanrec.nebula.version_db', 'vault', vault_rv_version='1.16.2') | from_json }}"
"""

RETURN = """
---
_raw:
    description:
        - A one-element list containing a JSON encoded object with the resolved
          C(download_link), C(version) and, when available, C(checksum) and C(extras).
    type: list
    elements: str
"""

display = Display()


class LookupModule(LookupBase):
    """
    Lookup module that retrieves version details.
    """

    def run(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, terms: list[str], variables: dict[str, Any] | None = None, **kwargs: dict[str, Any]
    ) -> list[str]:
        """
        Run the lookup module.
        """

        self.set_options(var_options=variables, direct=kwargs)  # pyright: ignore[reportUnknownMemberType]

        if not terms:
            raise AnsibleLookupError("No terms provided for lookup")

        if len(terms) > 1:
            raise AnsibleLookupError(f"Only one term is allowed for lookup, got {len(terms)}, {terms}")

        version_details: VersionDetails
        try:
            version_details = get_version(  # pyright: ignore[reportUnknownVariableType]
                app_name=terms[0], variables=variables, **kwargs
            )
        except Exception as e:
            raise AnsibleLookupError(f"Failed to get version details for {terms[0]}: {str(e)}") from e

        return [json.dumps(version_details)]  # type: ignore
