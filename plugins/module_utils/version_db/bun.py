#!/usr/bin/python3
"""
This module provides the Bun class, which extends the AppDetails class to fetch
bun releases.

Classes:
    Bun: A class to fetch and manage bun application details.

Bun class:
    Attributes:
        __github_repo (str): The GitHub repository for bun.
        __github_release_tag_prefix (str): The prefix of the bun release tags.
        __bun_architecture_map (dict): A mapping of architecture names to bun architecture names.

    Methods:
        fetch_details(): Fetches the bun version details from GitHub or uses the provided version tag.

"""

from __future__ import annotations

from ansible.utils.display import Display  # type: ignore

from .grs import github_release_tag_search

# pylint: disable=E0401,E0611
from .models import AppDetails  # type: ignore

display = Display()


class Bun(AppDetails):
    """
    bun app details.
    """

    __github_repo: str = "oven-sh/bun"

    __github_release_tag_prefix: str = "bun-v"

    __bun_architecture_map: dict[str, str] = {
        "amd64": "x64",
        "x86_64": "x64",
        "aarch64": "aarch64",
    }

    def fetch_details(self) -> None:
        _github_release_tag = self._kwargs.get("bun_rv_version", None)
        if not _github_release_tag or _github_release_tag == self._FETCH_LATEST_KEY:
            display.vvv("AppDetails bun: Fetching bun version details from GitHub.")
            # pylint: disable=R0801
            _github_release_tag = github_release_tag_search(
                github_release_tag_search_repo=self.__github_repo,
                github_release_tag_search_api_url=self._kwargs.get("github_release_tag_search_api_url"),
                github_release_tag_search_token=self._kwargs.get("github_release_tag_search_token"),
                github_release_tag_search_prefix=self.__github_release_tag_prefix,
                github_release_tag_search_contains=self._kwargs.get("github_release_tag_search_contains"),
                github_release_tag_search_max_pages=int(self._kwargs.get("github_release_tag_search_max_pages", 100)),
                github_release_tag_search_timeout=self._kwargs.get("github_release_tag_search_timeout", 10),
            )[len(self.__github_release_tag_prefix) :]
        else:
            display.vvv(f"AppDetails bun: Using provided bun version tag: {_github_release_tag}")

        _archive_name = f"bun-linux-{self._get_ansible_architecture(self.__bun_architecture_map)}"
        _release_url = (
            f"https://github.com/oven-sh/bun/releases/download/{self.__github_release_tag_prefix}{_github_release_tag}"
        )
        # pylint: disable=attribute-defined-outside-init
        self._download_link = f"{_release_url}/{_archive_name}.zip"
        self._checksum = f"sha256:{_release_url}/SHASUMS256.txt"
        self._extras = {"archive_dir": _archive_name}

        self._version = _github_release_tag
