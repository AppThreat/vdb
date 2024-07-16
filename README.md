# Introduction

Pre-built databases:

- purl2cpe database for [cdxgen](https://github.com/CycloneDX/cdxgen) - Unused
- vulnerability database for [dep-scan](https://github.com/AppThreat/dep-scan), including OS and application vulnerabilities. The following VDB settings were used:

- NVD_START_YEAR: 2018 or 2014 (10y)
- GITHUB_PAGE_COUNT: 5 or 10 (10y)

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

Use the name suffix `-10y`, to download a larger database with data from 2014.

```bash
export VDB_HOME=$HOME/vdb
# ghcr.io/appthreat/vdbzst-10y:v6
oras pull ghcr.io/appthreat/vdbxz-10y:v6 -o $VDB_HOME
tar -xvf *.tar.xz
rm *.tar.xz
```

dep-scan would automatically use this database for all the scans using the environment variable `VDB_HOME`.

## Private on-premise registry

A private registry is usually not required since the entire vdb comprises only two files - an index and a db. Any mounted share is usually sufficient. If you are looking for your private registry, you can try [Zot Registry](https://zotregistry.io/v1.4.3/). In addition to Zot, ORAS cli can work with [many](https://oras.land/docs/adopters) OCI-native container image registries.
