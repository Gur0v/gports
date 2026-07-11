pkgname = "ugrd"
pkgver = "2.2.0"
pkgrel = 2
build_style = "python_pep517"
hostmakedepends = ["python-build", "python-installer", "python-setuptools"]
checkdepends = ["python-installer", "python-pycpio", "python-zenlib"]
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
# Full upstream integration tests require privileged filesystem fixtures.
# Run only the package's focused non-privileged regressions.
options = ["etcfiles"]


def check(self):
    self.rm(".cbuild-checkenv", recursive=True, force=True)
    self.do(
        "python3",
        "-m",
        "venv",
        "--system-site-packages",
        "--clear",
        ".cbuild-checkenv",
    )
    envpy = self.chroot_cwd / ".cbuild-checkenv/bin/python3"
    whl = [str(p.relative_to(self.cwd)) for p in self.cwd.glob("dist/*.whl")]
    self.do(envpy, "-m", "installer", *whl)
    self.do(envpy, "tests/test_musl.py", path=[envpy.parent])
    self.do("python3", "tests/test_posix_shell.py")
    self.do("python3", "tests/test_usb_keyboard.py")


def post_install(self):
    self.install_file("examples/example.toml", "etc/ugrd", name="config.toml")
    self.install_file(
        "completion/ugrd", "usr/share/bash-completion/completions"
    )
    self.install_file("completion/_ugrd", "usr/share/zsh/site-functions")
    self.install_license("LICENSE")
