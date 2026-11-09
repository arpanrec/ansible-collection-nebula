# DEVELOPMENT Notes

## Development Setup

Install dependencies, including the dev extras:

```bash
uv sync --extra dev
```

## LSP Support for module_utils

Search for `uv run python -m site` to find the location of the site-packages directory. This is where the `ansible` and `ansible_collections` packages are installed.

Command to find the location of the site-packages directory:

```bash
uv run python -m site
```

Output:

```shell
sys.path = [
    '/home/arpan/Projects/ansible-collection-nebula',
    '/home/arpan/.local/share/uv/python/cpython-3.14.7-linux-x86_64-gnu/lib/python314.zip',
    '/home/arpan/.local/share/uv/python/cpython-3.14.7-linux-x86_64-gnu/lib/python3.14',
    '/home/arpan/.local/share/uv/python/cpython-3.14.7-linux-x86_64-gnu/lib/python3.14/lib-dynload',
    '/home/arpan/Projects/ansible-collection-nebula/.venv/lib/python3.14/site-packages',
]
USER_BASE: '/home/arpan/.local' (exists)
USER_SITE: '/home/arpan/.local/lib/python3.14/site-packages' (doesn't exist)
ENABLE_USER_SITE: False
```

Create a symlink of the `arpanrec.nebula` directory to the `ansible_collections` directory in the `site-packages` directory.

```bash
rm -rf "$(pwd)/.venv/lib/python3.14/site-packages/ansible_collections/arpanrec"
mkdir -p "$(pwd)/.venv/lib/python3.14/site-packages/ansible_collections/arpanrec/nebula"
ln -s "$(pwd)/plugins" "$(pwd)/.venv/lib/python3.14/site-packages/ansible_collections/arpanrec/nebula/plugins"
```

## Releasing

Cut a release from a clean `main`:

```bash
scripts/release.sh 1.26.0
git push origin main 1.26.0
```

The script writes the version into `galaxy.yml`, `pyproject.toml`, `uv.lock` and the install example in `README.md`,
regenerates `requirements.txt` and `requirements-dev.txt`, then commits `chore(release): <version>` and tags it. Pushing
the tag runs the release workflow. It creates the GitHub release, checks that the tag matches the `galaxy.yml` version,
publishes the collection to Ansible Galaxy and attaches the archive to the release.
