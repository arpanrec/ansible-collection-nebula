#!/usr/bin/python3
"""
This module defines the models for version database management in the Nebula plugin.

Classes:
    SupportedApps(enum.Enum): Enum representing supported applications.
    VersionDetails(Dict[str, Any]): Dictionary to hold version details.
    AppDetails(abc.ABC): Abstract base class for application details.

Classes Details:
    SupportedApps:
        Enum Members:
            - BWS: Represents the 'bws' application.
            - TERRAFORM: Represents the 'terraform' application.
            - VAULT: Represents the 'vault' application.
            - GO: Represents the 'go' application.
            - JAVA: Represents the 'java' application.
            - NODEJS: Represents the 'nodejs' application.
            - PULUMI: Represents the 'pulumi' application.
            - GITEA: Represents the 'gitea' application.
            - HADOLINT: Represents the 'hadolint' application.
            - GITLEAKS: Represents the 'gitleaks' application.
            - UV: Represents the 'uv' application.
            - RCLONE: Represents the 'rclone' application.

    VersionDetails:
        A dictionary to store version details of an application.

    AppDetails:
        Abstract base class to define the structure for application details.

        Attributes:
            _variables (Optional[Dict[str, Any]]): Variables related to the application.
            _download_link (str): Download link for the application.
            _version (str): Version of the application.
            _args (Tuple[Any, ...]): Arguments for the application.
            _extras (Optional[Dict[str, Any]]): Extra details for the application.
            _kwargs (Dict[str, Any]): Keyword arguments for the application.
            _checksum (Optional[str]): Checksum for the application.
            _FETCH_LATEST_KEY (str): Key to fetch the latest version.

        Methods:
            __init__(*args, **kwargs): Initializes the AppDetails instance.
            fetch_details(): Abstract method to fetch version details for the app.
            _get_ansible_architecture(ansible_to_expected: Optional[Dict[str, str]] = None) -> str:
                Retrieves the architecture from Ansible facts.
            get_version_details() -> VersionDetails:
                Retrieves the version details for the app.

"""

from __future__ import annotations

import abc
import enum
import json
from typing import Any

from ansible.utils.display import Display  # type: ignore

display = Display()


class SupportedApps(enum.Enum):
    """
    Supported apps.
    """

    BWS = "bws"
    TERRAFORM = "terraform"
    VAULT = "vault"
    GO = "go"
    JAVA = "java"
    NODEJS = "nodejs"
    PULUMI = "pulumi"
    GITEA = "gitea"
    HADOLINT = "hadolint"
    GITLEAKS = "gitleaks"
    UV = "uv"
    RCLONE = "rclone"


class VersionDetails(dict[str, Any]):
    """
    Version details.
    """


class AppDetails(abc.ABC):
    """
    App details.
    """

    __metaclass__ = abc.ABCMeta

    _variables: dict[str, Any] | None
    _download_link: str
    _version: str
    _args: tuple[Any, ...]
    _extras: dict[str, Any] | None = None
    _kwargs: dict[str, Any]
    _checksum: str | None = None
    _FETCH_LATEST_KEY = "fetch_latest_version"

    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        """
        Constructor.
        """

        self._variables = kwargs.get("variables")  # pyright: ignore[reportUnknownMemberType]
        self._args = args
        self._kwargs = kwargs

    @abc.abstractmethod
    def fetch_details(self) -> None:
        """
        Get the version details for the app.
        """

    def _get_ansible_architecture(self, ansible_to_expected: dict[str, str] | None = None) -> str:
        """
        Get the architecture from the Ansible facts.
        """

        display.vvv("AppDetails Get Ansible Architecture: Fetching Ansible architecture.")

        if not self._variables:
            raise ValueError("Hostvars not provided.")

        if not self._variables.get("ansible_architecture", None):
            raise ValueError("ansible_architecture not found in hostvars. Make sure gather_facts is enabled.")

        ansible_architecture: str = self._variables["ansible_architecture"]
        display.vvv(f"AppDetails Get Ansible Architecture: Ansible architecture: {ansible_architecture}")

        if not ansible_to_expected:
            display.vvv(
                f"AppDetails Get Ansible Architecture: Ansible architecture selected as: {ansible_architecture}"
            )
            return ansible_architecture

        if ansible_architecture not in ansible_to_expected:
            raise ValueError(
                f"Unsupported architecture: {ansible_architecture}, Supported Only in:"
                f" {json.dumps(ansible_to_expected)}"
            )
        display.vvv(
            f"AppDetails Get Ansible Architecture: Ansible architecture selected as"
            f": {ansible_to_expected[ansible_architecture]}"
        )
        return ansible_to_expected[ansible_architecture]

    def get_version_details(self) -> VersionDetails:
        """
        Get the version details for the app.
        """

        display.vvv("AppDetails: Getting version details.")

        version_details: VersionDetails = VersionDetails()
        version_details["download_link"] = self._download_link
        version_details["version"] = self._version
        if self._checksum:
            version_details["checksum"] = self._checksum
        if self._extras:
            version_details["extras"] = self._extras

        display.vvv(f"AppDetails: Version details: {version_details}")
        return version_details
