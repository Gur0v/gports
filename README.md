# gports

`gports` is a personal Chimera Linux ports collection. It contains package
templates and uses a nearby checkout of
[cports](https://github.com/chimera-linux/cports) as the cbuild engine and the
upstream dependency tree. It does not fork or duplicate cports.

## Requirements

Use Chimera Linux with `git`, `cports`, and `ruff` installed. By default the
checkouts must be siblings:

```text
Projects/
├── cports/
└── gports/
```

Set `CPORTS_DIR=/path/to/cports` if the cports checkout is elsewhere.

## First-time setup

1. Set your name in `etc/config.ini` and configure an **absolute** signing-key
   path, for example:

   ```ini
   [build]
   maintainer = Your Name <you@example.org>

   [signing]
   key = /home/you/Projects/gports/etc/keys/gports.rsa
   ```

2. Generate the key using cbuild:

   ```sh
   ../cports/cbuild --config "$PWD/etc/config.ini" keygen
   ```

   The private key remains in `etc/keys/` and is ignored by Git. To trust
   packages built by this repository locally:

   ```sh
   doas mkdir -p /etc/apk/keys
   doas install -m 0644 etc/keys/gports.rsa.pub /etc/apk/keys/
   ```

3. Bootstrap the local cbuild root once:

   ```sh
   ./gbuild bootstrap
   ```

## Build a port

`gbuild` temporarily exposes every `gports/user/*` template to cports, so
packages in this repository can depend on one another. Package names must not
collide with `cports/user` package names.

```sh
./gbuild lint user/ugrd
./gbuild pkg user/ugrd
```

The `ugrd` port builds `python-zenlib` and `python-pycpio` automatically. Built
APKs are placed below `packages/user/<architecture>/`.

Templates follow cports' 80-column Ruff/Black rules. Check them before a build:

```sh
ruff check user/
ruff format --check user/
```

## Install local packages

```sh
printf '%s\n' '@gports /absolute/path/to/gports/packages/user' \
    | doas tee /etc/apk/repositories.d/gports.list
apk add ugrd@gports
```

## Add a port

1. Copy `templates/template.py.example` to `user/<name>/template.py`.
2. Fill in metadata, dependencies, source URL, and SHA-256.
3. Run `./gbuild lint user/<name>` then `./gbuild pkg user/<name>`.

`cports/Packaging.md` is the package-template API reference; `cports/Usage.md`
documents cbuild commands and behavior.

## Included ports

- `ugrd` — µgRD 2.2.0; installs its default `/etc/ugrd/config.toml` and shell
  completions. Its privileged upstream test suite is intentionally disabled.
- `python-zenlib` and `python-pycpio` — ugRD's runtime dependencies.

See `user/ugrd/README.md` for Chimera-specific ugRD usage notes.
