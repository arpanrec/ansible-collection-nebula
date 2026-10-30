#!/usr/bin/python3
"""
Module to search GitHub repository releases for the latest matching release tag.
"""

from __future__ import annotations

import os
import re

import httpx
from ansible.utils.display import Display  # type: ignore

display = Display()

# A hyphen right after a digit starts a semver pre-release suffix, e.g. "v2.0.0-rc.1" or "v27.0.0-alpha.0".
# Prefix hyphens such as "bws-v1.0.0" or "bun-v1.2.3" don't follow a digit, so they don't match.
_PRE_RELEASE_SUFFIX_PATTERN = re.compile(r"\d-[0-9A-Za-z]")


def has_pre_release_suffix(version_tag: str) -> bool:
    """
    Check if a version tag carries a semver pre-release suffix (alpha, beta, rc, nightly, etc.).

    Args:
        version_tag (str): The version tag to check.

    Returns:
        bool: True if the tag has a pre-release suffix.
    """
    return bool(_PRE_RELEASE_SUFFIX_PATTERN.search(version_tag))


# pylint: disable=R0912,R0913,R0914,R0915
def github_release_tag_search(
    *,
    github_release_tag_search_repo: str,
    github_release_tag_search_api_url: str | None,
    github_release_tag_search_token: str | None,
    github_release_tag_search_prefix: str | None = None,
    github_release_tag_search_suffix: str | None = None,
    github_release_tag_search_contains: str | None = None,
    github_release_tag_search_max_pages: int | None = 100,
    github_release_tag_search_timeout: int | None = 10,
) -> str:
    """
    Search for the latest release in a GitHub repository.

    Releases flagged as pre-release on GitHub, and tags with a semver pre-release suffix, are skipped.

    Args:
        github_release_tag_search_repo (str): The GitHub repository to search.
        github_release_tag_search_token (str):
            The GitHub token to authenticate with. Optional.
            Default is the `GITHUB_TOKEN` environment variable.
        github_release_tag_search_api_url (str): The GitHub API URL. Optional. Default is "https://api.github.com".
        github_release_tag_search_prefix (str): The prefix of the tag to search for. Optional.
        github_release_tag_search_suffix (str): The suffix of the tag to search for. Optional.
        github_release_tag_search_contains (str): The substring that the tag should contain. Optional.
        github_release_tag_search_max_pages (int): The maximum number of pages to search. Optional. Default is 100.
        github_release_tag_search_timeout (int): The timeout in seconds. Optional. Default is 10.

    Raises:
        ValueError:
            If no matching tag is found.
            If no releases are found for the repository.

    Returns:
        str: The latest tag in the GitHub repository.
    """
    display.vvv(f"github_release_tag_search: Searching for latest release in {github_release_tag_search_repo}")
    if not github_release_tag_search_token:
        display.vvv(
            "github_release_tag_search: No GitHub token provided."
            " Trying to fetch github token from environment variable 'GITHUB_TOKEN'."
        )
        github_release_tag_search_token = os.getenv("GITHUB_TOKEN", None)

        if github_release_tag_search_token:
            display.vvv("github_release_tag_search: GitHub token fetched from environment")

    if not github_release_tag_search_token:
        display.warning("github_release_tag_search: No GitHub token provided. Rate limits may apply.")

    if not github_release_tag_search_api_url:
        github_release_tag_search_api_url = "https://api.github.com"

    display.vvv(f"github_release_tag_search: GitHub API URL: {github_release_tag_search_api_url}")

    if not github_release_tag_search_max_pages or github_release_tag_search_max_pages < 1:
        github_release_tag_search_max_pages = 100

    if not github_release_tag_search_timeout or github_release_tag_search_timeout < 1:
        github_release_tag_search_timeout = 10

    tag_version: str | None = None
    url: str = f"{github_release_tag_search_api_url}/repos/{github_release_tag_search_repo}/releases"
    headers: dict[str, str] = {"Accept": "application/vnd.github.v3+json", "X-GitHub-Api-Version": "2022-11-28"}

    if github_release_tag_search_token:
        headers["Authorization"] = f"Bearer {github_release_tag_search_token}"

    params: dict[str, str | int] = {
        "per_page": 50,
    }
    page_num: int = 0

    while page_num < github_release_tag_search_max_pages:
        page_num += 1
        params["page"] = page_num

        response = httpx.get(url, headers=headers, params=params, timeout=github_release_tag_search_timeout)
        response.raise_for_status()
        response_data = response.json()
        if len(response_data) == 0:
            if page_num == 1:
                raise ValueError(f"No releases found for {github_release_tag_search_repo}")
            display.vvv("github_release_tag_search: Reached the last page of releases, stopping search.")
            break
        for release in response_data:
            pre_release: bool = bool(release.get("prerelease", False))

            if pre_release:
                continue

            tag_name = release.get("tag_name")

            if tag_name:
                if has_pre_release_suffix(tag_name):
                    display.vvv(f"github_release_tag_search: Skipping pre-release tag: {tag_name}")
                    continue

                if github_release_tag_search_prefix and not tag_name.startswith(github_release_tag_search_prefix):
                    continue

                if github_release_tag_search_suffix and not tag_name.endswith(github_release_tag_search_suffix):
                    continue

                if github_release_tag_search_contains and github_release_tag_search_contains not in tag_name:
                    continue

                tag_version = tag_name
                display.vvv(f"github_release_tag_search: Found tag: {tag_version}")
                break

        if tag_version:
            display.vvv(f"github_release_tag_search: Found tag: {tag_version}")
            break

    if not tag_version or len(tag_version) < 1:
        raise ValueError(f"github_release_tag_search: No matching tag found for {github_release_tag_search_repo}")

    display.vvv(f"github_release_tag_search: Latest tag found: {tag_version}")
    return tag_version
