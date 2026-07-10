#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM

mkdir -p "$tmp/cports/user"
printf '#!/bin/sh\nexit 0\n' > "$tmp/cports/cbuild"
chmod +x "$tmp/cports/cbuild"

CPORTS_DIR="$tmp/cports" "$root/gbuild" lint user/ugrd
for package in python-pycpio python-zenlib ugrd; do
    test ! -e "$tmp/cports/user/$package"
done

mkdir "$tmp/cports/user/python-zenlib"
if CPORTS_DIR="$tmp/cports" "$root/gbuild" lint user/ugrd 2>/dev/null; then
    exit 1
fi
test ! -e "$tmp/cports/user/python-pycpio"
test -d "$tmp/cports/user/python-zenlib"
