# Introduction

Pre-built vulnerability database for [dep-scan](https://github.com/AppThreat/dep-scan)

## Manual download

To download this database manually, use the [ORAS cli](https://oras.land/cli/)

```
export VDB_HOME=$HOME/vdb
oras pull ghcr.io/ngcloudsec/vdb:v1 -o $VDB_HOME
```

dep-scan would automatically use this database for all the scans.
