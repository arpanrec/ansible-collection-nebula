#!/usr/bin/python3
"""
This module provides the Uv class, which extends the AppDetails class to fetch
uv releases.

Classes:
    Uv: A class to fetch and manage uv application details.

Uv class:
    Attributes:
        __github_repo (str): The GitHub repository for uv.
        __uv_architecture_map (dict): A mapping of architecture names to uv release target triples.

    Methods:
        fetch_details(): Fetches the uv version details from GitHub or uses the provided version tag.

"""

from __future__ import annotations

from ansible.utils.display import Display  # type: ignore

from .grs import github_release_tag_search

# pylint: disable=E0401,E0611
from .models import AppDetails  # type: ignore

display = Display()


class Uv(AppDetails):
    """
    uv app details.
    """

    __github_repo: str = "astral-sh/uv"

    __uv_architecture_map: dict[str, str] = {
        "amd64": "x86_64-unknown-linux-gnu",
        "x86_64": "x86_64-unknown-linux-gnu",
        "aarch64": "aarch64-unknown-linux-gnu",
    }

    def fetch_details(self) -> None:
        _github_release_tag = self._kwargs.get("uv_rv_version", None)
        if not _github_release_tag or _github_release_tag == self._FETCH_LATEST_KEY:
            display.vvv("AppDetails uv: Fetching uv version details from GitHub.")
            # pylint: disable=R0801
            _github_release_tag = github_release_tag_search(
                github_release_tag_search_repo=self.__github_repo,
                github_release_tag_search_api_url=self._kwargs.get("github_release_tag_search_api_url"),
                github_release_tag_search_token=self._kwargs.get("github_release_tag_search_token"),
                github_release_tag_search_contains=self._kwargs.get("github_release_tag_search_contains"),
                github_release_tag_search_max_pages=int(self._kwargs.get("github_release_tag_search_max_pages", 100)),
                github_release_tag_search_timeout=self._kwargs.get("github_release_tag_search_timeout", 10),
            )
        else:
            display.vvv(f"AppDetails uv: Using provided uv version tag: {_github_release_tag}")
        # pylint: disable=attribute-defined-outside-init
        self._download_link = (
            f"https://github.com/astral-sh/uv/releases/download/{_github_release_tag}"
            f"/uv-{self._get_ansible_architecture(self.__uv_architecture_map)}.tar.gz"
        )

        self._version = _github_release_tag
