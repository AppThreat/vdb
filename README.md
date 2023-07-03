# Introduction

Pre-built databases:

- purl2cpe database for [cdxgen](https://github.com/CycloneDX/cdxgen) - Unused
- vulnerability database for [dep-scan](https://github.com/AppThreat/dep-scan), including OS and application vulnerabilities. The following VDB settings were used:

- NVD_START_YEAR: 2018
- GITHUB_PAGE_COUNT: 5

## Manual download

To download this database manually, use the [ORAS cli](https://oras.land/cli/)

```bash
export VDB_HOME=$HOME/vdb
oras pull public.ecr.aws/appthreat/vdb:v5 -o $VDB_HOME
# oras pull public.ecr.aws/appthreat/purl2cpe:v1 -o $VDB_HOME
```

```bash
export VDB_HOME=$HOME/vdb
oras pull ghcr.io/appthreat/vdb:v5 -o $VDB_HOME
# oras pull ghcr.io/appthreat/purl2cpe:v1 -o $VDB_HOME
```

dep-scan would automatically use this database for all the scans using the environment variable `VDB_HOME`.

## Private on-premise registry

A private registry is usually not required since the entire vdb comprises of only two files - an index and a db. Any mounted share is usually sufficient. If you are looking for your own private registry, you can try [Zot Registry](https://zotregistry.io/v1.4.3/). In addition to Zot, ORAS cli can work with [many](https://oras.land/docs/adopters) OCI-native container image registries.
