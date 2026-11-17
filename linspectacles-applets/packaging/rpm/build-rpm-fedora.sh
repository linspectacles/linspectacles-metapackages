#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd -- "$HERE/../.." && pwd)"
REPO_ROOT="$(cd -- "$PACKAGE_ROOT/.." && pwd)"
NAME="linspectacles-applets"
SPEC="$HERE/$NAME.spec"
MODE="${1:---all}"
KEEP_BUILD="${KEEP_BUILD:-0}"
OUT="${RPM_OUTPUT_DIR:-$HERE/dist-rpm}"
BUILD_PARENT="${RPM_TOPDIR:-/var/tmp}"

usage() {
  cat <<'USAGE'
Usage: build-rpm-fedora.sh [--all|--prepare-only]

--all            Build binary RPM and SRPM (default; requires rpmbuild).
--prepare-only   Generate the RPM spec and source tarball without rpmbuild.

RPM_TOPDIR      Existing, whitespace-free parent directory for a temporary work tree.
RPM_OUTPUT_DIR  Directory receiving RPMs, source tarball, and generated spec.
KEEP_BUILD=1    Keep the private RPM work tree for debugging.
USAGE
}

case "$MODE" in
  --all|--prepare-only) ;;
  -h|--help) usage; exit 0 ;;
  *) usage >&2; exit 2 ;;
esac

if [[ ! -f "$SPEC" || ! -f "$REPO_ROOT/LICENSE" || ! -f "$PACKAGE_ROOT/README.md" ]]; then
  echo "ERROR: spec, repository LICENSE, or linspectacles-applets README.md is missing" >&2
  exit 2
fi
if [[ "$MODE" != '--prepare-only' ]] && ! command -v rpmbuild >/dev/null 2>&1; then
  echo 'Missing prerequisite: rpmbuild (Fedora: sudo dnf install rpm-build)' >&2
  exit 2
fi
if [[ "$BUILD_PARENT" =~ [[:space:]] || ! -d "$BUILD_PARENT" ]]; then
  echo 'ERROR: RPM_TOPDIR must be an existing, whitespace-free parent directory.' >&2
  exit 2
fi

VERSION="$(awk '$1 == "Version:" { print $2; exit }' "$SPEC")"
if [[ ! "$VERSION" =~ ^[A-Za-z0-9._+~]+$ ]]; then
  echo "ERROR: invalid or missing spec Version: $VERSION" >&2
  exit 2
fi

TOPDIR="$(mktemp -d -- "$BUILD_PARENT/linspectacles-applets-metapackage-rpm.XXXXXXXX")"
cleanup() {
  if [[ "$KEEP_BUILD" == '1' ]]; then
    echo "RPM work tree kept at: $TOPDIR"
  else
    rm -rf -- "$TOPDIR"
  fi
}
trap cleanup EXIT

mkdir -p "$TOPDIR"/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS} "$OUT"
PKG_STEM="$NAME-$VERSION"
STAGE="$TOPDIR/SOURCES/$PKG_STEM"
mkdir -p "$STAGE"
cp -- "$REPO_ROOT/LICENSE" "$STAGE/LICENSE"
cp -- "$PACKAGE_ROOT/README.md" "$STAGE/README.md"
cp -- "$SPEC" "$TOPDIR/SPECS/$NAME.spec"
tar -czf "$TOPDIR/SOURCES/$PKG_STEM.tar.gz" -C "$TOPDIR/SOURCES" "$PKG_STEM"
rm -rf -- "$STAGE"
cp -- "$TOPDIR/SOURCES/$PKG_STEM.tar.gz" "$OUT/"
cp -- "$TOPDIR/SPECS/$NAME.spec" "$OUT/"

if [[ "$MODE" == '--prepare-only' ]]; then
  echo "Prepared RPM inputs: $OUT"
  exit 0
fi

rpmbuild -ba --define "_topdir $TOPDIR" "$TOPDIR/SPECS/$NAME.spec"
find "$TOPDIR/RPMS" "$TOPDIR/SRPMS" -type f \
  \( -name '*.rpm' -o -name '*.src.rpm' \) \
  -exec cp -a {} "$OUT/" \;

echo "RPM/SRPM artifacts: $OUT"
