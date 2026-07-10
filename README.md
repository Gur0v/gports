# gports

`gports` is an independent collection of Chimera Linux package templates. It
uses a nearby clone of [cports](https://github.com/chimera-linux/cports) as the
build engine and dependency tree; only templates and generated artifacts owned
by this collection live here.

## Prerequisites

You need a Chimera system (or a supported cbuild host), `git`, and a sibling
`cports` checkout:

```text
Projects/
├── cports/
└── gports/
```

If cports is elsewhere, set `CPORTS_DIR` before invoking `gbuild`.

## Quick start

The included package proves the wiring without downloading or compiling
anything:

```sh
./gbuild lint user/gports-bootstrap
./gbuild pkg user/gports-bootstrap
```

Generate a signing key before distributing packages. Set an **absolute** key
path in `etc/config.ini`, for example
`key = /home/you/Projects/gports/etc/keys/gports.rsa`, then run
`$CPORTS_DIR/cbuild --config "$PWD/etc/config.ini" keygen`. The `etc/keys/`
directory is ignored by Git. Copy only its `.pub` file to `/etc/apk/keys/` on
machines that will consume your repository.

## Add a real package

1. Copy `templates/template.py.example` into `user/<name>/template.py`.
2. Set accurate metadata, build dependencies, source URL, and SHA-256.
3. Run `./gbuild prepare-upgrade user/<name>` to fetch sources and update the
   checksum, then review the template change.
4. Run `./gbuild lint user/<name>` and `./gbuild pkg user/<name>`.
5. Install the result from `packages/user`:

   ```sh
   printf '%s\n' '@gports /absolute/path/to/gports/packages/user' \
       | sudo tee /etc/apk/repositories.d/gports.list
   sudo install -m 0644 etc/keys/*.pub /etc/apk/keys/
   apk add <name>@gports
   ```

`gbuild` temporarily creates a symlink in the cports `user/` directory while a
command runs. It removes it on exit. A gports package name must therefore not
collide with an existing `cports/user` package.

## Layout

```text
user/<name>/template.py  package definition
user/<name>/files/       extra installed files
user/<name>/patches/     source patches
templates/               copyable starting points
packages/                generated APK repository (ignored)
```

For build styles, package fields, and helper APIs, consult the matching version
of `cports/Packaging.md`; `cports/Usage.md` documents every cbuild command.
