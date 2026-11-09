#!/usr/bin/python3
"""
This module provides functionality to fetch and manage Vault application details.

Classes:
    Vault: Inherits from AppDetails and provides methods to fetch Vault version details.

Attributes:
    __vault_releases_url (str): URL to fetch Vault release versions.
    __vault_ansible_architecture_map (Dict[str, str]): Mapping of Ansible architecture to Vault architecture.

Methods:
    fetch_details(self) -> None:
        Fetches the version details for the Vault application. If a specific version is not provided,
        it fetches the latest version available. Constructs the download link for the Vault binary
        based on the fetched or provided version and the system architecture.

"""

from __future__ import annotations

from typing import Any

import httpx
from ansible.utils.display import Display  # type: ignore
from packaging.version import Version

from .models import AppDetails  # type: ignore

display = Display()


class Vault(AppDetails):  # pylint: disable=too-few-public-methods
    """
    Vault app details.
    """

    __vault_releases_url: str = "https://releases.hashicorp.com/vault/index.json"

    __vault_ansible_architecture_map: dict[str, str] = {"x86_64": "amd64", "aarch64": "arm64"}

    def fetch_details(self) -> None:
        """
        Get the version details for the Vault.
        """
        _vault_release_tag = self._kwargs.get("vault_rv_version", None)
        if not _vault_release_tag or _vault_release_tag == self._FETCH_LATEST_KEY:
            display.vvv(f"Fetching Vault version details from {self.__vault_releases_url}.")
            try:
                _expected_version: str | None = None
                _vault_releases: dict[str, Any] = httpx.get(self.__vault_releases_url, timeout=10).json()["versions"]
                for key in list(_vault_releases.keys()):
                    # pylint: disable=R0801
                    if ("+" in key) or ("beta" in key) or ("rc" in key) or ("oci" in key) or ("alpha" in key):
                        continue
                    if not _expected_version:
                        _expected_version = key
                    else:
                        if Version(key) > Version(_expected_version):
                            _expected_version = key

                if not _expected_version:
                    raise ValueError("Failed to fetch Vault releases.")
                _vault_release_tag = _expected_version
                display.vvv(f"Latest Vault release tag: {_vault_release_tag}")

            except Exception as e:
                display.error(f"Failed to fetch Vault releases: {e}")
                raise ValueError(f"Failed to fetch Vault releases. {str(e)}") from e
        else:
            display.vvv(f"Using provided Vault version tag: {_vault_release_tag}")
        # https://releases.hashicorp.com/vault/1.4.4/vault_1.4.4_linux_amd64.zip
        # pylint: disable=attribute-defined-outside-init
        self._download_link = (
            f"https://releases.hashicorp.com/vault/{_vault_release_tag}"
            f"/vault_{_vault_release_tag}_linux_"
            f"{self._get_ansible_architecture(self.__vault_ansible_architecture_map)}.zip"
        )
        self._version = _vault_release_tag
