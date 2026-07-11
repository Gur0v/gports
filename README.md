# gports

Personal Chimera Linux packages built with an adjacent
[cports](https://github.com/chimera-linux/cports) checkout. Packaging policy,
tools, dependencies, and documentation come from cports; this repository keeps
only packages absent there or requiring a narrow local patch.

## Setup

Keep both repositories beside each other, or set `CPORTS_DIR`:

```text
Projects/
├── cports/
└── gports/
```

Create the ignored local configuration from cports, then set your maintainer and
signing key:

```sh
cp "${CPORTS_DIR:-../cports}/etc/config.ini.example" etc/config.ini
$EDITOR etc/config.ini
"${CPORTS_DIR:-../cports}/cbuild" --config "$PWD/etc/config.ini" keygen
./gbuild bootstrap
```

The signing key belongs in `etc/keys/`. Both it and `etc/config.ini` are ignored. Install only the public key on systems that consume the repository:

```sh
doas mkdir -p /etc/apk/keys
doas install -m 0644 etc/keys/gports.rsa.pub /etc/apk/keys/
```

## Build

`gbuild` exposes these templates to cports' `user` category for one command.
Package names cannot collide with `cports/user`.

```sh
./gbuild lint user/ugrd
./gbuild pkg user/ugrd
```

See cports' `Usage.md` and `Packaging.md` for everything else.

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
