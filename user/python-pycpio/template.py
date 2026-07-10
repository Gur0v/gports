pkgname = "python-pycpio"
pkgver = "1.7.0"
pkgrel = 0
build_style = "python_pep517"
hostmakedepends = ["python-build", "python-installer", "python-setuptools"]
depends = ["python", "python-zenlib>=3.3.0"]
checkdepends = ["python-installer", "python-zenlib"]
pkgdesc = "Python library for reading and writing cpio archives"
license = "GPL-2.0-only"
url = "https://github.com/desultory/pycpio"
source = f"{url}/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "64234e0c4221f3c801c793a9cd6e902c93f1b4a8428723dd98b41f3d2a46fdf1"


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
    self.do(
        envpy,
        "-P",
        "-m",
        "unittest",
        "discover",
        "tests",
        "-v",
        path=[envpy.parent],
    )


def post_install(self):
    self.install_license("LICENSE")
