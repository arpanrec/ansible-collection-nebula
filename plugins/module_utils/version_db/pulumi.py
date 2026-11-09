#!/usr/bin/python3
"""
This module provides the Pulumi class, which extends the AppDetails class to fetch
and manage Pulumi application details.

Classes:
    Pulumi: A class to fetch and manage Pulumi application details.

Pulumi class:
    Attributes:
        __github_repo (str): The GitHub repository for Pulumi.
        __pulumi_architecture_map (dict): A mapping of architecture names to Pulumi architecture names.

    Methods:
        fetch_details(): Fetches the Pulumi version details from GitHub or uses the provided version tag.

"""

from __future__ import annotations

from ansible.utils.display import Display  # type: ignore

from .grs import github_release_tag_search  # type: ignore

# pylint: disable=E0401,E0611
from .models import AppDetails  # type: ignore

display = Display()


class Pulumi(AppDetails):
    """
    Pulumi app details.
    """

    __github_repo: str = "pulumi/pulumi"

    __pulumi_architecture_map: dict[str, str] = {
        "amd64": "x64",
        "x86_64": "x64",
        "aarch64": "arm64",
    }

    def fetch_details(self) -> None:
        _github_release_tag = self._kwargs.get("pulumi_rv_version", None)
        if not _github_release_tag or _github_release_tag == self._FETCH_LATEST_KEY:
            display.vvv("AppDetails Pulumi: Fetching Pulumi version details from GitHub.")
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
            display.vvv(f"AppDetails Pulumi: Using provided Pulumi version tag: {_github_release_tag}")

        # pylint: disable=attribute-defined-outside-init
        self._download_link = (
            f"https://github.com/pulumi/pulumi/releases/download/{_github_release_tag}"
            f"/pulumi-{_github_release_tag}"
            f"-linux-{self._get_ansible_architecture(self.__pulumi_architecture_map)}.tar.gz"
        )

        self._version = _github_release_tag
