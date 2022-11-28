# Introduction

Pre-built vulnerability database for [dep-scan](https://github.com/AppThreat/dep-scan). The database is built on a `self-hosted` runner since github hosted runners are failing to handle the database size which is over 3 GB.

## Manual download

To download this database manually, use the [ORAS cli](https://oras.land/cli/)

```
export VDB_HOME=$HOME/vdb
oras pull ghcr.io/ngcloudsec/vdb:v1 -o $VDB_HOME
```

dep-scan would automatically use this database for all the scans.
