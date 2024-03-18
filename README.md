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
oras pull ghcr.io/appthreat/vdb:v6 -o $VDB_HOME
```

Use the name `vdb-10y`, to download a larger database with data from 2014.

```bash
export VDB_HOME=$HOME/vdb
oras pull ghcr.io/appthreat/vdb-10y:v6 -o $VDB_HOME
```

dep-scan would automatically use this database for all the scans using the environment variable `VDB_HOME`.

## .tar.gz compressed database

Use the tar.gz compressed database to reduce the download time. depscan would soon use this version as the default.

```bash
export VDB_HOME=$HOME/vdb
oras pull ghcr.io/appthreat/vdbgz:v6 -o $VDB_HOME
tar -xvf *.tar.gz
rm *.tar.gz
```

## Registry Accelerated File System (RAFS) format

vdb is also available in a high-performance compression format called RAFS created using [nydus](https://nydus.dev). On Linux and Intel Mac, use the [nydus-image tool](https://github.com/dragonflyoss/nydus/releases/latest) to unpack and convert the vdb data into a tar file as shown.

```bash
export VDB_HOME=$HOME/vdb
export RAFS_OUT=rafs_out
oras pull ghcr.io/appthreat/vdb:v6-rafs -o $RAFS_OUT
nydus-image unpack --blob $RAFS_OUT/data.rafs --output $VDB_HOME/vdb.tar --bootstrap $RAFS_OUT/meta.rafs
tar -C $VDB_HOME -xf $VDB_HOME/vdb.tar
rm $VDB_HOME/vdb.tar
```

When using depscan, the above steps are performed automatically based on the presence of `nydus-image` in the PATH.

## Private on-premise registry

A private registry is usually not required since the entire vdb comprises of only two files - an index and a db. Any mounted share is usually sufficient. If you are looking for your private registry, you can try [Zot Registry](https://zotregistry.io/v1.4.3/). In addition to Zot, ORAS cli can work with [many](https://oras.land/docs/adopters) OCI-native container image registries.
