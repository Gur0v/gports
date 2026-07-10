# gports

`gports` is a small personal package collection for Chimera Linux. The sibling [cports](https://github.com/chimera-linux/cports) checkout remains the build system, dependency tree, and authoritative source for packaging policy. This repository holds only packages that are not in cports, or that need a local, narrowly scoped change.

## Setup

Keep the repositories beside each other, or set `CPORTS_DIR` to the cports checkout:

```text
Projects/
├── cports/
└── gports/
```

The tracked `etc/config.ini.example` and `pyproject.toml` are copied unchanged from cports. Create the ignored personal configuration and change only local values such as `maintainer` and the signing key:

```sh
cp etc/config.ini.example etc/config.ini
$EDITOR etc/config.ini
../cports/cbuild --config "$PWD/etc/config.ini" keygen
./gbuild bootstrap
```

The signing key belongs in `etc/keys/`. Both it and `etc/config.ini` are ignored. Install only the public key on systems that consume the repository:

```sh
doas mkdir -p /etc/apk/keys
doas install -m 0644 etc/keys/gports.rsa.pub /etc/apk/keys/
```

## Build

cbuild does not support external collections directly. `gbuild` is a thin bridge: it exposes all gports templates under cports' `user` category for one command, then removes the links. Package names therefore cannot collide with `cports/user`.

```sh
./gbuild lint user/ugrd
./gbuild pkg user/ugrd
```

All template fields, patch handling, checks, repositories, and dependencies come from cbuild. Refer to `../cports/Usage.md` and `../cports/Packaging.md`; gports intentionally does not duplicate those docs.

## Install

Add the generated repository and its public key, then install through APK:

```sh
printf '%s\n' '@gports /absolute/path/to/gports/packages/user' \
    | doas tee /etc/apk/repositories.d/gports.list
doas apk update
doas apk add ugrd@gports
```

## Packages

- `ugrd`: µgRD with narrowly scoped Chimera/musl and Btrfs compatibility patches.
- `python-zenlib` and `python-pycpio`: runtime dependencies required by ugRD, currently absent from cports.
