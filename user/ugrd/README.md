# ugRD on Chimera

This port deliberately installs ugRD itself, its default configuration, and
shell completions only. Upstream's `installkernel` hook is Gentoo-specific, and
the `kernel-install` hook targets systemd's kernel-install protocol, neither of
which is Chimera's default initramfs integration.

Build the initramfs explicitly after installing the package, for example:

```sh
doas ugrd /boot/initramfs-"$(uname -r)".img
```

Review `/etc/ugrd/config.toml` before building it, especially on an encrypted
root filesystem. Optional runtime functionality requires its matching Chimera
packages (for example `cryptsetup`, `lvm2`, `btrfs-progs`, `zfs`, or
`python-zstandard`).
