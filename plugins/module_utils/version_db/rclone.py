#!/usr/bin/python3
"""
This module provides the Rclone class, which extends the AppDetails class to fetch
rclone releases.

Classes:
    Rclone: A class to fetch and manage rclone application details.

Rclone class:
    Attributes:
        __github_repo (str): The GitHub repository for rclone.
        __rclone_architecture_map (dict): A mapping of architecture names to rclone architecture names.

    Methods:
        fetch_details(): Fetches the rclone version details from GitHub or uses the provided version tag.

"""

from __future__ import annotations

from ansible.utils.display import Display  # type: ignore

from .grs import github_release_tag_search

# pylint: disable=E0401,E0611
from .models import AppDetails  # type: ignore

display = Display()


class Rclone(AppDetails):
    """
    rclone app details.
    """

    __github_repo: str = "rclone/rclone"

    __rclone_architecture_map: dict[str, str] = {
        "amd64": "amd64",
        "x86_64": "amd64",
        "aarch64": "arm64",
    }

    def fetch_details(self) -> None:
        _github_release_tag = self._kwargs.get("rclone_rv_version", None)
        if not _github_release_tag or _github_release_tag == self._FETCH_LATEST_KEY:
            display.vvv("AppDetails rclone: Fetching rclone version details from GitHub.")
            # pylint: disable=R0801
            _github_release_tag = github_release_tag_search(
                github_release_tag_search_repo=self.__github_repo,
                github_release_tag_search_api_url=self._kwargs.get("github_release_tag_search_api_url"),
                github_release_tag_search_token=self._kwargs.get("github_release_tag_search_token"),
                github_release_tag_search_contains=self._kwargs.get("github_release_tag_search_contains"),
                github_release_tag_search_max_pages=int(self._kwargs.get("github_release_tag_search_max_pages", 100)),
                github_release_tag_search_timeout=self._kwargs.get("github_release_tag_search_timeout", 10),
            )[1:]
        else:
            display.vvv(f"AppDetails rclone: Using provided rclone version tag: {_github_release_tag}")

        _archive_name = (
            f"rclone-v{_github_release_tag}-linux-{self._get_ansible_architecture(self.__rclone_architecture_map)}"
        )
        _release_url = f"https://github.com/rclone/rclone/releases/download/v{_github_release_tag}"
        # pylint: disable=attribute-defined-outside-init
        self._download_link = f"{_release_url}/{_archive_name}.zip"
        self._checksum = f"sha256:{_release_url}/SHA256SUMS"
        self._extras = {"archive_dir": _archive_name}

        self._version = _github_release_tag
