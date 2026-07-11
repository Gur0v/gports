pkgname = "modprobed-db"
pkgver = "2.50"
pkgrel = 0
build_style = "makefile"
makedepends = ["dinit-chimera"]
depends = ["bash", "kmod"]
pkgdesc = "Track loaded kernel modules for localmodconfig"
license = "MIT"
url = "https://github.com/graysky2/modprobed-db"
source = f"{url}/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "8cd9b490896a5e1e3eddf9c5a7dd771de8627965ffad0ca6426d25c886d904ee"
# no test suite
options = ["!check"]


def post_install(self):
    self.uninstall("usr/lib/systemd/user")
    self.install_service(self.files_path / "modprobed-db.user")
    self.install_license("MIT")
