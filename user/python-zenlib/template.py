pkgname = "python-zenlib"
pkgver = "3.3.0"
pkgrel = 0
build_style = "python_pep517"
hostmakedepends = ["python-build", "python-installer", "python-setuptools"]
depends = ["python"]
checkdepends = ["python-installer"]
pkgdesc = "Python library with reusable utility functions"
license = "GPL-2.0-only"
url = "https://github.com/desultory/zenlib"
source = f"{url}/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "ae51ed55ae67783d5f7d015a79c303c4a1f70b27defe4bdb1f9c55dea3197c3a"


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
        env={"CI": "true"},
        path=[envpy.parent],
    )


def post_install(self):
    self.install_license("LICENSE")
