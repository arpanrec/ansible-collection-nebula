#!/usr/bin/python3
"""
This module provides functionality to retrieve version details for various supported applications.

Classes:
    Display: Utility class from ansible.utils.display for displaying messages.
    AppDetails: Base class for application details.
    SupportedApps: Enum class representing supported applications.
    VersionDetails: Class representing version details of an application.

Functions:
    get_version(app_name: str, *args, **kwargs) -> VersionDetails:

        Parameters:
            app_name (str): The name of the application.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            VersionDetails: An instance containing version details of the specified application.

        Raises:
            ValueError: If the specified app is not supported.

"""

from __future__ import annotations

from ansible.utils.display import Display  # type: ignore

from .models import AppDetails, SupportedApps, VersionDetails

display = Display()


def get_version(app_name: str, *args, **kwargs) -> VersionDetails:  # type: ignore # pylint: disable=R0914,too-many-branches
    """
    Get the version details for the specified app.
    """
    app_details: AppDetails | None = None

    match app_name:
        case SupportedApps.BWS.value:
            from .bws import BWS  # pylint: disable=import-outside-toplevel

            app_details = BWS(*args, **kwargs)  # type: ignore

        case SupportedApps.TERRAFORM.value:
            from .terraform import Terraform  # pylint: disable=import-outside-toplevel

            app_details = Terraform(*args, **kwargs)  # type: ignore

        case SupportedApps.VAULT.value:
            from .vault import Vault  # pylint: disable=import-outside-toplevel

            app_details = Vault(*args, **kwargs)  # type: ignore

        case SupportedApps.GO.value:
            from .go import Go  # pylint: disable=import-outside-toplevel

            app_details = Go(*args, **kwargs)  # type: ignore

        case SupportedApps.JAVA.value:
            from .java import Java  # pylint: disable=import-outside-toplevel

            app_details = Java(*args, **kwargs)  # type: ignore

        case SupportedApps.NODEJS.value:
            from .nodejs import NodeJS  # pylint: disable=import-outside-toplevel

            app_details = NodeJS(*args, **kwargs)  # type: ignore

        case SupportedApps.PULUMI.value:
            from .pulumi import Pulumi  # pylint: disable=import-outside-toplevel

            app_details = Pulumi(*args, **kwargs)  # type: ignore

        case SupportedApps.GITEA.value:
            from .gitea import Gitea  # pylint: disable=import-outside-toplevel

            app_details = Gitea(*args, **kwargs)  # type: ignore

        case SupportedApps.HADOLINT.value:
            from .hadolint import Hadolint  # pylint: disable=import-outside-toplevel

            app_details = Hadolint(*args, **kwargs)  # type: ignore

        case SupportedApps.GITLEAKS.value:
            from .gitleaks import Gitleaks  # pylint: disable=import-outside-toplevel

            app_details = Gitleaks(*args, **kwargs)  # type: ignore

        case SupportedApps.UV.value:
            from .uv import Uv  # pylint: disable=import-outside-toplevel

            app_details = Uv(*args, **kwargs)  # type: ignore

        case SupportedApps.RCLONE.value:
            from .rclone import Rclone  # pylint: disable=import-outside-toplevel

            app_details = Rclone(*args, **kwargs)  # type: ignore

        case SupportedApps.BUN.value:
            from .bun import Bun  # pylint: disable=import-outside-toplevel

            app_details = Bun(*args, **kwargs)  # type: ignore

        case SupportedApps.BETTERLEAKS.value:
            from .betterleaks import Betterleaks  # pylint: disable=import-outside-toplevel

            app_details = Betterleaks(*args, **kwargs)  # type: ignore

        case _:
            raise ValueError(f"Unsupported app: {app_name}")

    if not app_details:
        raise ValueError(f"Unsupported app: {app_name}")

    app_details.fetch_details()
    version_details: VersionDetails = app_details.get_version_details()

    return version_details
