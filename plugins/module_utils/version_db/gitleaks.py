#!/usr/bin/python3
"""
This module provides the gitleaks class, which extends the AppDetails class to fetch
gitleaks releases.

Classes:
    Gitleaks: A class to fetch and manage gitleaks application details.

gitleaks class:
    Attributes:
        __github_repo (str): The GitHub repository for gitleaks.
        __gitleaks_architecture_map (dict): A mapping of architecture names to gitleaks architecture names.

    Methods:
        fetch_details(): Fetches the gitleaks version details from GitHub or uses the provided version tag.

"""

from __future__ import annotations

from ansible.utils.display import Display  # type: ignore

from .grs import github_release_tag_search

# pylint: disable=E0401,E0611
from .models import AppDetails  # type: ignore

display = Display()


class Gitleaks(AppDetails):
    """
    gitleaks app details.
    """

    __github_repo: str = "gitleaks/gitleaks"

    __gitleaks_architecture_map: dict[str, str] = {
        "amd64": "x64",
        "x86_64": "x64",
        "aarch64": "arm64",
    }

    def fetch_details(self) -> None:
        _github_release_tag = self._kwargs.get("gitleaks_rv_version", None)
        if not _github_release_tag or _github_release_tag == self._FETCH_LATEST_KEY:
            display.vvv("AppDetails gitleaks: Fetching gitleaks version details from GitHub.")
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
            display.vvv(f"AppDetails gitleaks: Using provided gitleaks version tag: {_github_release_tag}")
        # pylint: disable=attribute-defined-outside-init
        self._download_link = (
            f"https://github.com/gitleaks/gitleaks/releases/download/v{_github_release_tag}"
            f"/gitleaks_{_github_release_tag}_linux_"
            f"{self._get_ansible_architecture(self.__gitleaks_architecture_map)}.tar.gz"
        )

        self._version = _github_release_tag
