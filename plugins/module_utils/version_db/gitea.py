#!/usr/bin/python3
"""
This module provides the Gitea class, which extends the AppDetails class to fetch
gitea releases.

Classes:
    Gitea: A class to fetch and manage Gitea application details.

Gitea class:
    Attributes:
        __github_repo (str): The GitHub repository for Gitea.
        __gitea_architecture_map (dict): A mapping of architecture names to Gitea architecture names.

    Methods:
        fetch_details(): Fetches the Gitea version details from GitHub or uses the provided version tag.

"""

from __future__ import annotations

from ansible.utils.display import Display  # type: ignore

from .grs import github_release_tag_search

# pylint: disable=E0401,E0611
from .models import AppDetails  # type: ignore

display = Display()


class Gitea(AppDetails):
    """
    Gitea app details.
    """

    __github_repo: str = "go-gitea/gitea"

    __gitea_architecture_map: dict[str, str] = {
        "amd64": "amd64",
        "x86_64": "amd64",
        "aarch64": "arm64",
    }

    def fetch_details(self) -> None:
        _github_release_tag = self._kwargs.get("gitea_rv_version", None)
        if not _github_release_tag or _github_release_tag == self._FETCH_LATEST_KEY:
            display.vvv("AppDetails gitea: Fetching gitea version details from GitHub.")
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
            display.vvv(f"AppDetails gitea: Using provided gitea version tag: {_github_release_tag}")
        # pylint: disable=attribute-defined-outside-init
        self._download_link = (
            f"https://github.com/go-gitea/gitea/releases/download/v{_github_release_tag}"
            f"/gitea-{_github_release_tag}-linux-{self._get_ansible_architecture(self.__gitea_architecture_map)}"
        )

        self._version = _github_release_tag
