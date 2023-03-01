# Introduction

Pre-built vulnerability database for [dep-scan](https://github.com/AppThreat/dep-scan) including OS and application vulnerabilities. Following VDB settings were used:

- NVD_START_YEAR: 2018
- GITHUB_PAGE_COUNT: 5

## Manual download

To download this database manually, use the [ORAS cli](https://oras.land/cli/)

```
export VDB_HOME=$HOME/vdb
oras pull ghcr.io/appthreat/vdb:v5 -o $VDB_HOME
```

dep-scan would automatically use this database for all the scans.
