"""
This Ansible filter plugin classifies a flat list of strings into the
C(subject_alt_name) entries expected by C(community.crypto.openssl_csr).
"""

from __future__ import annotations

import ipaddress
import re

DOCUMENTATION = """
name: san_list_transformer
short_description: Prefix each entry of a list with the SAN type community.crypto.openssl_csr expects.
version_added: "1.7.0"
description:
    - Classify each string in a flat list as an IP address, an email address, or a DNS name, and
      prefix it accordingly (C(IP:), C(email:), or C(DNS:)) so the result can be passed directly as
      the C(subject_alt_name) option of C(community.crypto.openssl_csr).
    - Each entry is checked with Python's C(ipaddress) module first (matches both IPv4 and IPv6),
      then against a practical email pattern, and falls back to C(DNS:) otherwise.
options:
    _input:
        description:
            - A flat list of strings (hostnames, IP addresses, and/or email addresses).
        required: true
        type: list
        elements: str
"""

EXAMPLES = """
- name: Build a subject_alt_name list from mixed hostnames, IPs, and an email
  ansible.builtin.debug:
      msg: "{{ ['nextcloud', '10.8.33.201', 'admin@example.com'] | san_list_transformer }}"

# {"...": ["DNS:nextcloud", "IP:10.8.33.201", "email:admin@example.com"]}

- name: A loopback IP is still classified as an IP entry
  ansible.builtin.debug:
      msg: "{{ ['nextcloud', '127.0.0.1'] | san_list_transformer }}"

# {"...": ["DNS:nextcloud", "IP:127.0.0.1"]}
"""

RETURN = r"""
_value:
    description: The input list, with each entry prefixed by its SAN type.
    type: list
    elements: str
"""

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def san_list_transformer(items: list[str]) -> list[str]:
    """
    Prefix each entry with IP:, email:, or DNS: for use as an openssl_csr subject_alt_name list.
    """
    result: list[str] = []
    for item in items:
        try:
            parsed_ip = ipaddress.ip_address(item)
        except ValueError:
            parsed_ip = None

        if parsed_ip is not None:
            result.append(f"IP:{item}")
            continue

        if _EMAIL_PATTERN.match(item):
            result.append(f"email:{item}")
            continue

        result.append(f"DNS:{item}")
    return result


class FilterModule:  # pylint: disable=too-few-public-methods
    """
    A filter plugin for Ansible.
    """

    def filters(self) -> dict[str, object]:
        """
        Return a dictionary mapping filter names to functions.
        """
        return {
            "san_list_transformer": san_list_transformer,
        }
