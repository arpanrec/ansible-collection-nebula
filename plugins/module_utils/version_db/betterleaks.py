#!/usr/bin/python3
"""
This module provides the Betterleaks class, which extends the AppDetails class to fetch
betterleaks releases.

Classes:
    Betterleaks: A class to fetch and manage betterleaks application details.

Betterleaks class:
    Attributes:
        __github_repo (str): The GitHub repository for betterleaks.
        __github_release_tag_prefix (str): The prefix of the betterleaks release tags.
        __betterleaks_architecture_map (dict): A mapping of architecture names to betterleaks architecture names.

    Methods:
        fetch_details(): Fetches the betterleaks version details from GitHub or uses the provided version tag.

"""

from __future__ import annotations

from ansible.utils.display import Display  # type: ignore

from .grs import github_release_tag_search

# pylint: disable=E0401,E0611
from .models import AppDetails  # type: ignore

display = Display()


class Betterleaks(AppDetails):
    """
    betterleaks app details.
    """

    __github_repo: str = "betterleaks/betterleaks"

    __github_release_tag_prefix: str = "v"

    __betterleaks_architecture_map: dict[str, str] = {
        "amd64": "x64",
        "x86_64": "x64",
        "aarch64": "arm64",
    }

    def fetch_details(self) -> None:
        _github_release_tag = self._kwargs.get("betterleaks_rv_version", None)
        if not _github_release_tag or _github_release_tag == self._FETCH_LATEST_KEY:
            display.vvv("AppDetails betterleaks: Fetching betterleaks version details from GitHub.")
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
            display.vvv(f"AppDetails betterleaks: Using provided betterleaks version tag: {_github_release_tag}")

        _release_url = (
            f"https://github.com/betterleaks/betterleaks/releases/download/"
            f"{self.__github_release_tag_prefix}{_github_release_tag}"
        )
        # pylint: disable=attribute-defined-outside-init
        self._download_link = (
            f"{_release_url}/betterleaks_{_github_release_tag}_linux_"
            f"{self._get_ansible_architecture(self.__betterleaks_architecture_map)}.tar.gz"
        )
        self._checksum = f"sha256:{_release_url}/checksums.txt"

        self._version = _github_release_tag
