#!/usr/bin/python3
"""
This module provides the Pnpm class, which extends the AppDetails class to fetch
pnpm releases.

Classes:
    Pnpm: A class to fetch and manage pnpm application details.

Pnpm class:
    Attributes:
        __github_repo (str): The GitHub repository for pnpm.
        __github_release_tag_prefix (str): The prefix of the pnpm release tags.
        __pnpm_architecture_map (dict): A mapping of architecture names to pnpm architecture names.

    Methods:
        fetch_details(): Fetches the pnpm version details from GitHub or uses the provided version tag.

"""

from __future__ import annotations

from ansible.utils.display import Display  # type: ignore

from .grs import github_release_tag_search

# pylint: disable=E0401,E0611
from .models import AppDetails  # type: ignore

display = Display()


class Pnpm(AppDetails):
    """
    pnpm app details.
    """

    __github_repo: str = "pnpm/pnpm"

    # Tags of other packages released from the same repository (for example ``pnpr@...``) do not start with "v".
    __github_release_tag_prefix: str = "v"

    __pnpm_architecture_map: dict[str, str] = {
        "amd64": "x64",
        "x86_64": "x64",
        "aarch64": "arm64",
    }

    def fetch_details(self) -> None:
        _github_release_tag = self._kwargs.get("pnpm_rv_version", None)
        if not _github_release_tag or _github_release_tag == self._FETCH_LATEST_KEY:
            display.vvv("AppDetails pnpm: Fetching pnpm version details from GitHub.")
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
            display.vvv(f"AppDetails pnpm: Using provided pnpm version tag: {_github_release_tag}")

        # pnpm releases do not publish a checksum file, so no checksum is set.
        # pylint: disable=attribute-defined-outside-init
        self._download_link = (
            f"https://github.com/pnpm/pnpm/releases/download/{self.__github_release_tag_prefix}{_github_release_tag}/"
            f"pnpm-linux-{self._get_ansible_architecture(self.__pnpm_architecture_map)}.tar.gz"
        )

        self._version = _github_release_tag
