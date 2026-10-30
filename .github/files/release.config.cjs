module.exports = {
    branches: ['main'],
    tagFormat: '${version}',
    plugins: [
        [
            '@semantic-release/commit-analyzer',
            {
                preset: 'angular',
                parserOpts: {
                    noteKeywords: ['BREAKING CHANGE', 'BREAKING CHANGES', 'BREAKING'],
                },
            },
        ],
        [
            '@semantic-release/release-notes-generator',
            {
                preset: 'angular',
                parserOpts: {
                    noteKeywords: ['BREAKING CHANGE', 'BREAKING CHANGES', 'BREAKING'],
                },
                writerOpts: {
                    commitsSort: ['subject', 'scope'],
                },
            },
        ],
        [
            '@semantic-release/exec',
            {
                prepareCmd: [
                    "sed -i 's/^version:.*/version: ${nextRelease.version}/g' galaxy.yml",
                    "sed -i 's/^export NEBULA_VERSION=.*/export NEBULA_VERSION=${nextRelease.version}/g' README.md",
                    'uv version ${nextRelease.version}',
                    'uv export --format requirements-txt --no-hashes --no-annotate --no-header --no-emit-project --no-progress --no-group dev -o requirements.txt',
                    'uv export --format requirements-txt --no-hashes --no-annotate --no-header --no-emit-project --no-progress -o requirements-dev.txt',
                    'uv --offline run --no-sync --no-progress ansible-galaxy collection build',
                ].join(' && '),
                successCmd:
                    'uv --offline run --no-sync --no-progress ansible-galaxy collection publish arpanrec-nebula-${nextRelease.version}.tar.gz --api-key ${process.env.GALAXY_API_KEY}',
            },
        ],
        [
            '@semantic-release/changelog',
            {
                changelogFile: 'CHANGELOG.md',
            },
        ],
        [
            '@semantic-release/git',
            {
                assets: [
                    'galaxy.yml',
                    'CHANGELOG.md',
                    'pyproject.toml',
                    'uv.lock',
                    'README.md',
                    'requirements.txt',
                    'requirements-dev.txt',
                ],
                message: 'chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}',
            },
        ],
        [
            '@semantic-release/github',
            {
                assets: [{ path: 'arpanrec-nebula-*.tar.gz' }],
            },
        ],
    ],
};
