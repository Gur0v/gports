pkgname = "ugrd"
pkgver = "2.2.0"
pkgrel = 0
build_style = "python_pep517"
hostmakedepends = ["python-build", "python-installer", "python-setuptools"]
depends = [
    "bash",
    "bc-gh",
    "kmod",
    "pax-utils",
    "python",
    "python-pycpio>=1.7.0",
    "python-zenlib>=3.3.0",
    "util-linux",
]
pkgdesc = "Minimal POSIX initramfs generator for encrypted systems"
license = "GPL-2.0-only"
url = "https://github.com/desultory/ugrd"
source = f"{url}/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "94a86adc6215e2c066d3384c3a5fa40bc0aa87cb786eead1bbb7a2d1c3b83a64"
# Upstream tests need privileged filesystem and kernel-tool fixtures.
options = ["etcfiles", "!check"]


def post_install(self):
    self.install_file("examples/example.toml", "etc/ugrd", name="config.toml")
    self.install_file(
        "completion/ugrd", "usr/share/bash-completion/completions"
    )
    self.install_file("completion/_ugrd", "usr/share/zsh/site-functions")
    self.install_license("LICENSE")
