# Introduction

Pre-built databases:

- vulnerability database for [dep-scan](https://github.com/AppThreat/dep-scan), including OS and application vulnerabilities. The following VDB settings were used:

- NVD_START_YEAR: 2020 or 2016 (10y db)
- GITHUB_PAGE_COUNT: 10, 20 (10y db), or 30 (app only db)

## Manual download

To download this database manually, use the [ORAS cli](https://oras.land/cli/)

```bash
export VDB_HOME=$HOME/vdb
oras pull ghcr.io/appthreat/vdbzst:v6 -o $VDB_HOME
zstd -d *.zst
rm *.zst
```

Or use the xz version.

```bash
export VDB_HOME=$HOME/vdb
oras pull ghcr.io/appthreat/vdbxz:v6 -o $VDB_HOME
tar -xvf *.tar.xz
rm *.tar.xz
```

Use the name suffix `-app`, to download a database containing only application vulnerabilities.

```bash
export VDB_HOME=$HOME/vdb
# ghcr.io/appthreat/vdbzst-app:v6
oras pull ghcr.io/appthreat/vdbxz-app:v6 -o $VDB_HOME
tar -xvf *.tar.xz
rm *.tar.xz
```

Use the name suffix `-10y`, to download a larger database with data from 2016.

```bash
export VDB_HOME=$HOME/vdb
# ghcr.io/appthreat/vdbzst-10y:v6
oras pull ghcr.io/appthreat/vdbxz-10y:v6 -o $VDB_HOME
tar -xvf *.tar.xz
rm *.tar.xz
```

## VDB 7 images

`build-vdb7.yml` publishes two kinds of artifact, and the difference decides
how you consume them.

**Complete databases** (`completeness=full`) — install as the main database:

| Image                                     | Scope                                  | Job                        |
| :---------------------------------------- | :------------------------------------- | :------------------------- |
| `ghcr.io/appthreat/vdb7-full`             | app + OS, everything incl. CPE         | `full_builder`             |
| `ghcr.io/appthreat/vdb7-app-only`         | app ecosystems, 2020+                  | `app_only_builder`         |
| `ghcr.io/appthreat/vdb7-app-extended`     | app ecosystems, 2020+, metadata tables | `app_extended_builder`     |
| `ghcr.io/appthreat/vdb7-app-10y`          | app ecosystems, 2016+                  | `app_10y_builder`          |
| `ghcr.io/appthreat/vdb7-app-10y-extended` | app ecosystems, 2016+, metadata tables | `app_10y_extended_builder` |

```bash
vdb db refresh full --app-only   # vdb7-app-only, the CLI default
vdb db refresh full --image ghcr.io/appthreat/vdb7-app-10y-extended:v7.0.x-xz
```

**Shards** (`completeness=partial`) — for the shard store only, placed with
`vdb db refresh <shard>`: `vdb7-deb`, `vdb7-rpm`, `vdb7-apk`, `vdb7-app`,
`vdb7-cpe` and one per purl type, all emitted by the `full_builder` job's
splitter. `vdb db refresh full` rejects them by design.

`vdb7-app` and `vdb7-app-only` are therefore different artifacts: the first is
a slice of the full database, the second a database built from an app-only
ingest. They used to share the `vdb7-app` repo and tag, which meant two jobs
raced every build and whichever finished last decided what `vdb7-app`
contained. Do not merge them back.

Tags follow the v7 convention: `v7.0.x-xz` / `v7.0.x-zst` for the pinned
release line and `v7-xz` / `latest-xz` (and zst equivalents) for the newest
build. Nothing publishes a bare `v7.0.x`. Every artifact is mirrored to the
Hugging Face dataset by `sync-vdb7-hf-from-oras.yml` under `v7-<name>/`;
`full`, `deb`, `rpm`, `apk` and the two `app-10y` variants are mirrored
compressed only, the rest also as raw `.vdb7`.

The 6.7.x line additionally publishes `-2y` and OS-inclusive `-extended` /
`-10y` images. Those have no v7 equivalent yet.

### Workflow scripts

Manifest handling lives in `.github/scripts/vdb7_meta.py`, shared by
`build-and-upload-vdb7` and `split-and-upload-vdb7`, rather than in inline
`python -c` blocks — see the script's docstring for the indentation and
quoting failures that motivated it.

dep-scan would automatically use this database for all the scans using the environment variable `VDB_HOME`.

## Private on-premise registry

A private registry is usually not required since the entire vdb comprises only two files - an index and a db. Any mounted share is usually sufficient. If you are looking for your private registry, you can try [Zot Registry](https://zotregistry.io/v1.4.3/). In addition to Zot, ORAS cli can work with [many](https://oras.land/docs/adopters) OCI-native container image registries.

