#!/usr/bin/python3
"""
This module provides functionality to fetch and manage NodeJS application details.

Classes:
    NodeJS(AppDetails): A class to handle NodeJS application details, including fetching version details from GitHub.

Methods:
    fetch_details(self) -> None:
        Fetches the NodeJS version details from GitHub or uses a provided version tag.
          Constructs the download link for the specified NodeJS version and architecture.

Attributes:
    __github_repo (str): The GitHub repository for NodeJS releases.
    __node_architecture_map (dict[str, str]): A mapping of architecture names to NodeJS architecture identifiers.
"""

from __future__ import annotations

import httpx
from ansible.utils.display import Display  # type: ignore

from .grs import has_pre_release_suffix

# pylint: disable=E0401,E0611
from .models import AppDetails  # type: ignore

display = Display()


class NodeJS(AppDetails):
    """
    NodeJS app details.
    """

    __node_dist_url = "https://nodejs.org/dist/index.json"

    __node_architecture_map: dict[str, str] = {
        "amd64": "x64",
        "x86_64": "x64",
        "armv7l": "armv7l",
        "aarch64": "arm64",
    }

    def fetch_details(self) -> None:
        _nodejs_version_tag = self._kwargs.get("nodejs_rv_version", None)
        if not _nodejs_version_tag or _nodejs_version_tag == self._FETCH_LATEST_KEY:
            display.vvv(f"AppDetails NodeJS: Fetching NodeJS version details from {self.__node_dist_url}")

            _nodejs_version_tags_res = httpx.get(self.__node_dist_url, timeout=10)

            if _nodejs_version_tags_res.status_code != 200:
                raise ValueError(f"Failed to fetch NodeJS version details: {_nodejs_version_tags_res.text}")

            _nodejs_version_tag = next(
                (
                    release["version"]
                    for release in _nodejs_version_tags_res.json()
                    if not has_pre_release_suffix(release["version"])
                ),
                None,
            )

            if not _nodejs_version_tag:
                raise ValueError(f"No stable NodeJS release found in {self.__node_dist_url}")

        else:
            display.vvv(f"AppDetails NodeJS: Using provided NodeJS version tag: {_nodejs_version_tag}")

        # pylint: disable=attribute-defined-outside-init
        self._download_link = (
            f"https://nodejs.org/download/release"
            f"/{_nodejs_version_tag}/node-{_nodejs_version_tag}-linux"
            f"-{self._get_ansible_architecture(self.__node_architecture_map)}.tar.gz"
        )
        self._version = _nodejs_version_tag
