#!/usr/bin/python3
"""
Ansible lookup plugin to get secrets
"""

from __future__ import annotations

import datetime
import json
import os
import subprocess  # nosec B404
from typing import Any

from ansible.errors import AnsibleLookupError  # type: ignore
from ansible.plugins.lookup import LookupBase  # type: ignore
from ansible.utils.display import Display  # type: ignore

try:
    from cachier import cachier  # pyright: ignore[reportUnknownVariableType]
except ImportError as e:
    raise AnsibleLookupError("Please install cachier with 'pip install cachier'") from e

# pylint: disable=invalid-name

DOCUMENTATION = """
---
name: arpanrec.nebula.bitwarden
author:
    - Arpan Mandal (@arpanrec) <arpan.rec@gmail.com>
requirements:
    - bw (command line utility)
    - be logged into bitwarden
    - bitwarden vault unlocked, or session key provided
    - cachier
    - Attachments are returned as the content of the file. Not the file/'file path' itself.
short_description: Retrieve secrets from Bitwarden
description:
    - Retrieve secrets from Bitwarden.
options:
    _terms:
        description: Key to fetch values for from login info.
        required: true
        type: list
        elements: str
    search:
        description:
            - Field to retrieve, for example V(name) or V(id).
            - If set to V(id), only zero or one element can be returned.
              Use the Jinja C(first) filter to get the only list element.
            - If set to V(None) or V(''), or if O(_terms) is empty, records are not filtered by fields.
        type: str
        default: name
    field:
        description:
            - Field to fetch. Leave unset to fetch whole response.
            - If set to V(username), V(password), V(totp), V(uri), or V(notes),
              only the value of that field is returned.
            - If set to a custom field name, the value of that field is returned.
            - Mutually exclusive with V(attachment_name) and V(attachment_id).
        type: str
    bw_session:
        description:
            - Pass session key instead of reading from env.
            - E(BW_SESSION) environment variable set.
            - Variable take precedence over environment variable.
        type: str
    attachment_name:
        description:
            - Name of the attachment to retrieve.
            - Mutually exclusive with V(field) and V(attachment_id).
        type: str
    attachment_id:
        description:
            - ID of the attachment to retrieve.
            - Mutually exclusive with V(field) and V(attachment_name).
        type: str
    secrets_lookup_cache_enabled:
        description:
            - Enable caching of the Bitwarden CLI output.
            - If set to V(true), V(yes), or V(1), caching is enabled.
            - If set to V(false), V(no), or V(0), caching is disabled.
            - pip install cachier required.
            - If enabled, then make sure to delete the cachier default cache directory after execution.
        type: bool
        default: false
"""

EXAMPLES = """
---
- name: "Get 'password' from all Bitwarden records named 'a_test'"
  ansible.builtin.debug:
      msg: "{{ lookup('arpanrec.nebula.bitwarden', 'a_test', field='password') }}"

- name: "Get 'password' from Bitwarden record with ID 'bafba515-af11-47e6-abe3-af1200cd18b2'"
  ansible.builtin.debug:
      msg: "{{ lookup('arpanrec.nebula.bitwarden', 'bafba515-af11-47e6-abe3-af1200cd18b2', search='id',
          field='password') }}"

- name: "Get list of all full Bitwarden records named 'a_test'"
  ansible.builtin.debug:
      msg: "{{ lookup('arpanrec.nebula.bitwarden', 'a_test') }}"

- name: "Get custom field 'api_key' from all Bitwarden records named 'a_test'"
  ansible.builtin.debug:
      msg: "{{ lookup('arpanrec.nebula.bitwarden', 'a_test', field='api_key') }}"

- name: "Get 'password' from all Bitwarden records named 'a_test', using given session key"
  ansible.builtin.debug:
      msg: "{{ lookup('arpanrec.nebula.bitwarden', 'a_test', field='password', bw_session='bXZ9B5TXi6...') }}"

- name: "Get a attachment named 'privkey.pem' from all Bitwarden records named 'a_test'"
  ansible.builtin.debug:
      msg: "{{ lookup('arpanrec.nebula.bitwarden', 'a_test', attachment_name='privkey.pem') }}"
"""

RETURN = """
---
_raw:
    description:
        - A one-element list that contains a list of requested fields or JSON objects of matches.
        - If you use C(query), you get a list of lists. If you use C(lookup) without C(wantlist=true),
          this always gets reduced to a list of field values or JSON objects.
    type: list
    elements: list
"""

display = Display()


class LookupModule(LookupBase):
    """
    Ansible lookup plugin to get secrets
    """

    __item: str
    __ret: str | None = None
    __search: str = "name"
    __cache_enabled: bool = False
    __bw_session: str | None = None

    def __get_custom_field(self, field_name: str) -> str:
        item_dict = json.loads(self.__bw_exec(["get", "item", self.__item]))
        fields: list[dict[str, Any]] = item_dict.get("fields", [])
        value: str | None = None
        for field in fields:
            if field["name"] == field_name:
                if value is not None:
                    raise AnsibleLookupError("Multiple fields with the same name found")
                value = field.get("value", None)
                if not value or len(value) == 0:
                    raise AnsibleLookupError("Field has no value")

        if not value:
            raise AnsibleLookupError("Field not found")

        return value

    def __get_attachment(self, attachment_name: str | None, attachment_id: str | None) -> str:
        item_dict: dict[str, Any] | None = None
        item_id: str
        if self.__search == "name":
            item_dict = dict(json.loads(self.__bw_exec(["get", "item", self.__item])))
            item_id = str(item_dict.get("id"))
        elif self.__search == "id":
            item_id = self.__item
        else:
            raise AnsibleLookupError("Invalid search type, only 'name' or 'id' is allowed")

        if not attachment_id:
            if not item_dict:
                item_dict = dict(json.loads(self.__bw_exec(["get", "item", item_id])))
            if not attachment_id and attachment_name:
                if "attachments" not in item_dict:
                    raise AnsibleLookupError("No attachments found")
                attachments: list[dict[str, Any]] = item_dict["attachments"]
                for att in attachments:
                    if attachment_name and att["fileName"] == attachment_name:
                        if attachment_id is not None:
                            raise AnsibleLookupError("Multiple attachments with the same name found")
                        attachment_id = att["id"]

        if not attachment_id:
            raise AnsibleLookupError("Attachment not found")

        attachment_str = self.__bw_exec(["get", "attachment", attachment_id, "--itemid", item_id])
        return attachment_str

    @cachier(stale_after=datetime.timedelta(minutes=60))
    def __bw_exec_with_cache(
        self,
        cmd: list[str],
        ret_encoding: str = "UTF-8",
        env_vars: dict[str, str] | None = None,
    ) -> str:
        """
        Executes a Bitwarden CLI command and returns the output as a string.
        """
        return self.__bw_exec_subprocess(cmd, ret_encoding, env_vars)

    def __bw_exec_without_cache(
        self,
        cmd: list[str],
        ret_encoding: str = "UTF-8",
        env_vars: dict[str, str] | None = None,
    ) -> str:
        """
        Executes a Bitwarden CLI command and returns the output as a string.
        """
        return self.__bw_exec_subprocess(cmd, ret_encoding, env_vars)

    def __bw_exec_subprocess(
        self,
        cmd: list[str],
        ret_encoding: str = "UTF-8",
        env_vars: dict[str, str] | None = None,
    ) -> str:
        """
        Executes a Bitwarden CLI command and returns the output as a string.
        """
        cmd = ["bw"] + cmd

        cmd.append("--raw")

        # Copy the environment instead of aliasing os.environ, otherwise updates
        # (including BW_SESSION) would leak into the controller process and persist
        # across subsequent lookups.
        cli_env_vars: dict[str, str] = dict(os.environ)

        if env_vars is not None:
            cli_env_vars.update(env_vars)

        if self.__bw_session:
            cli_env_vars["BW_SESSION"] = self.__bw_session

        display.vvv(f"Executing Bitwarden CLI command: {' '.join(cmd)}")
        command_out = subprocess.run(
            cmd, capture_output=True, check=False, encoding=ret_encoding, env=cli_env_vars, timeout=10
        )  # nosec B603
        if command_out.returncode != 0:
            raise AnsibleLookupError(
                "Bitwarden CLI command failed, error: " f"{command_out.stderr if len(command_out.stderr) > 0 else None}"
            )
        return command_out.stdout

    @staticmethod
    def __cache_dpath(cached_fn: Any) -> str:
        return cached_fn.cache_dpath()  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]

    def __bw_exec(
        self,
        cmd: list[str],
        ret_encoding: str = "UTF-8",
        env_vars: dict[str, str] | None = None,
    ) -> str:

        if self.__cache_enabled:
            cache_dpath = self.__cache_dpath(self.__bw_exec_with_cache)
            display.warning(
                f"Using cache location: '{cache_dpath}', Make sure to remove the directory after execution.\n"
            )
            return self.__bw_exec_with_cache(cmd, ret_encoding, env_vars)
        display.vvv("No cache location provided")
        return self.__bw_exec_without_cache(cmd, ret_encoding, env_vars)

    # pylint: disable=too-many-branches
    def run(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, terms: list[str] | None, variables: dict[str, Any] | None = None, **kwargs: dict[str, Any] | None
    ) -> list[str]:
        """
        get secrets
        """
        if not terms:
            raise AnsibleLookupError("No terms provided")

        if len(terms) != 1:
            raise AnsibleLookupError("Only one term is allowed")

        self.set_options(var_options=variables, direct=kwargs)  # pyright: ignore[reportUnknownMemberType]

        self.__item = terms[0]
        field: str | None = None
        attachment_name: str | None = None
        attachment_id: str | None = None

        if (
            variables
            and ("secrets_lookup_cache_enabled" in variables)
            and (str(variables["secrets_lookup_cache_enabled"]).lower() in ["true", "yes", "1"])
        ):
            self.__cache_enabled = True

        if variables and "bw_session" in variables:
            self.__bw_session = str(variables["bw_session"])

        if kwargs and len(kwargs) > 0:

            if "field" in kwargs:
                field = str(kwargs["field"])

            if "attachment_name" in kwargs:
                attachment_name = str(kwargs["attachment_name"])

            if "attachment_id" in kwargs:
                attachment_id = str(kwargs["attachment_id"])

            if "search" in kwargs:
                self.__search = str(kwargs["search"])
            if ("secrets_lookup_cache_enabled" in kwargs) and (
                str(kwargs["secrets_lookup_cache_enabled"]).lower() in ["true", "yes", "1"]
            ):
                self.__cache_enabled = True

            if "bw_session" in kwargs:
                self.__bw_session = str(kwargs["bw_session"])

        if not self.__bw_session and "BW_SESSION" in os.environ:
            self.__bw_session = os.environ["BW_SESSION"]

        if self.__search not in ["name", "id"]:
            raise AnsibleLookupError("Invalid search type, only 'name' or 'id' is allowed")

        if (attachment_name or attachment_id) and field:
            raise AnsibleLookupError("Only one of 'field' or ('attachment_name' or 'attachment_id') is allowed")

        if attachment_name and attachment_id:
            raise AnsibleLookupError("Only one of 'attachment_name' or 'attachment_id' is allowed")

        if not attachment_name and not attachment_id and not field:
            raise AnsibleLookupError("One of 'field' or 'attachment_name' or 'attachment_id' is required")

        if field in ["username", "password", "totp", "uri", "notes"]:
            self.__ret = self.__bw_exec(["get", field, self.__item])
        elif field:
            self.__ret = self.__get_custom_field(field)
        elif attachment_name or attachment_id:
            self.__ret = self.__get_attachment(attachment_name, attachment_id)
        else:
            raise AnsibleLookupError("Invalid field")

        if not self.__ret or len(self.__ret) == 0:
            raise AnsibleLookupError("No available fields found")

        # display.vvvvvv(f"Secrets: {self.__ret}, type: {type(self.__ret)}")

        return [str(self.__ret)]
