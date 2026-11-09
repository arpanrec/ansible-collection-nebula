#!/usr/bin/python3
"""
This module provides the `Go` class, which is a subclass of `AppDetails`.
 It is used to fetch the latest GoLang version details
   and construct the download link for the GoLang tarball based on the system architecture.

Classes:
    Go: A class to fetch and store GoLang application details.

Attributes:
    __go_version_endpoint (str): The endpoint URL to fetch the latest GoLang version.
    __go_version_endpoint_query (Dict[str, str]): The query parameters for the GoLang version endpoint.
    __go_ansible_architecture_map (Dict[str, str]):
      A mapping of Ansible architecture names to GoLang architecture names.

Methods:
    fetch_details(self) -> None:
        Fetches the latest GoLang version and constructs the download link for the GoLang tarball.

"""

from __future__ import annotations

import httpx
from ansible.utils.display import Display  # type: ignore

# pylint: disable=E0401,E0611
from .models import AppDetails  # type: ignore

display = Display()


class Go(AppDetails):  # pylint: disable=too-few-public-methods
    """
    GoLang app details.
    """

    # __go_version_endpoint = "https://golang.org/dl/?mode=json"
    __go_version_endpoint = "https://go.dev/VERSION"
    __go_version_endpoint_query: dict[str, str] = {"m": "text"}
    __go_ansible_architecture_map: dict[str, str] = {"x86_64": "amd64", "aarch64": "arm64"}

    def fetch_details(self) -> None:
        """
        Fetch the latest GoLang version.
        """

        display.vvv("AppDetails Go: Fetching GoLang version")
        _golang_release_tag = self._kwargs.get("go_rv_version", None)
        if not _golang_release_tag or _golang_release_tag == self._FETCH_LATEST_KEY:
            display.vvv(f"AppDetails Go: Fetching GoLang version details from {self.__go_version_endpoint}.")
            try:
                _golang_release_tag = httpx.get(
                    self.__go_version_endpoint, timeout=10, params=self.__go_version_endpoint_query
                ).text.splitlines()[0]

                display.vvv(f"AppDetails Go: Latest GoLang release tag: {_golang_release_tag}")

            except Exception as e:
                display.error(f"AppDetails Go: Failed to fetch GoLang releases: {e}")
                raise ValueError(f"AppDetails Go: Failed to fetch GoLang releases. {str(e)}") from e
        else:
            display.vvv(f"AppDetails Go: Using provided GoLang version tag: {_golang_release_tag}")
        # pylint: disable=attribute-defined-outside-init
        self._download_link = (
            f"https://go.dev/dl/{_golang_release_tag}.linux"
            f"-{self._get_ansible_architecture(self.__go_ansible_architecture_map)}.tar.gz"
        )
        self._version = _golang_release_tag
