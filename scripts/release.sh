#!/usr/bin/env bash
# Prepare a release: write the version into every file that carries it, commit, and tag.
# Pushing the tag starts .github/workflows/release.yml, which creates the GitHub release and publishes to Galaxy.
#
# Usage: scripts/release.sh <version>      e.g. scripts/release.sh 1.26.0

set -euo pipefail

usage() {
    echo "Usage: $0 <version>   (semantic version without a leading v, e.g. 1.26.0 or 1.26.0-rc.1)" >&2
    exit 1
}

[[ $# -eq 1 ]] || usage
version="$1"
semver_re='^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-[0-9A-Za-z.-]+)?$'
[[ "$version" =~ $semver_re ]] || usage

cd "$(git rev-parse --show-toplevel)"

branch="$(git branch --show-current)"
[[ "$branch" == "main" ]] || {
    echo "Releases are cut from main, not '${branch}'." >&2
    exit 1
}
[[ -z "$(git status --porcelain)" ]] || {
    echo "The working tree has uncommitted changes; commit or stash them first." >&2
    exit 1
}
if git rev-parse --quiet --verify "refs/tags/${version}" > /dev/null; then
    echo "Tag ${version} already exists." >&2
    exit 1
fi

current="$(sed -n 's/^version: *//p' galaxy.yml)"
echo "Bumping ${current} -> ${version}"

sed -i "s/^version:.*/version: ${version}/" galaxy.yml
sed -i "s/^export NEBULA_VERSION=.*/export NEBULA_VERSION=${version}/" README.md
uv version --no-progress "${version}"

export_args=(--format requirements-txt --no-hashes --no-annotate --no-header --no-emit-project --no-progress)
uv export "${export_args[@]}" --no-group dev -o requirements.txt
uv export "${export_args[@]}" -o requirements-dev.txt

git add galaxy.yml README.md pyproject.toml uv.lock requirements.txt requirements-dev.txt
git commit -m "chore(release): ${version}"
git tag "${version}"

echo
echo "Created commit and tag ${version}. Review with 'git show ${version}', then publish with:"
echo "    git push origin main ${version}"
