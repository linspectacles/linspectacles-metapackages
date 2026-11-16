#!/usr/bin/env python3
"""Dependency-free publication checks for linspectacles-metapackages 0.0.2."""

from pathlib import Path
import os
import re
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "linspectacles"
SPEC = PKG / "packaging/rpm/linspectacles.spec"
BUILD = PKG / "packaging/rpm/build-rpm-fedora.sh"
REPO = "https://github.com/linspectacles/linspectacles-metapackages"
HUB = "linspectacles-hub"
MODULES = "linspectacles-modules"
errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


def validate():
    required = [
        "README.md",
        "LICENSE",
        ".gitignore",
        ".github/REPOSITORY-ABOUT.md",
        ".github/workflows/validate.yml",
        "linspectacles/README.md",
        "linspectacles/packaging/rpm/README-RPM.md",
        "linspectacles/packaging/rpm/build-rpm-fedora.sh",
        "linspectacles/packaging/rpm/linspectacles.spec",
        "linspectacles-applets/README.md",
        "linspectacles-full/README.md",
        "tools/validate_repository.py",
    ]
    for rel in required:
        check((ROOT / rel).is_file(), f"missing repository file: {rel}")

    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    package_readme = (PKG / "README.md").read_text(encoding="utf-8")
    spec = SPEC.read_text(encoding="utf-8")
    about = (ROOT / ".github/REPOSITORY-ABOUT.md").read_text(encoding="utf-8")
    rpm_readme = (PKG / "packaging/rpm/README-RPM.md").read_text(encoding="utf-8")
    applets = (ROOT / "linspectacles-applets/README.md").read_text(encoding="utf-8")
    full = (ROOT / "linspectacles-full/README.md").read_text(encoding="utf-8")

    for name, content in [
        ("root README", root_readme),
        ("linspectacles README", package_readme),
        ("spec", spec),
        ("repository metadata", about),
        ("RPM README", rpm_readme),
    ]:
        check(REPO in content, f"{name} does not use canonical metapackages repository URL")

    check("Current repository release: **0.0.2**" in root_readme, "root README release is not 0.0.2")
    check("Current metapackage release: **0.0.2**" in package_readme, "package README release is not 0.0.2")
    check(re.search(r"^Name:\s+linspectacles$", spec, re.M) is not None, "spec package Name is not linspectacles")
    check(re.search(r"^Version:\s+0\.0\.2$", spec, re.M) is not None, "spec Version is not 0.0.2")
    check(re.search(r"^BuildArch:\s+noarch$", spec, re.M) is not None, "spec is not noarch")

    requires = re.findall(r"^Requires:\s+(\S+)(.*)$", spec, re.M)
    names = [name for name, _tail in requires]
    check(names == [HUB, MODULES], f"unexpected dependency composition/order: {names}")
    check(all(not tail.strip() for _name, tail in requires), "dependency version constraints were added")
    check("linspectacles-applets" not in names, "WIP applets package became a dependency prematurely")
    check("linspectacles-full" not in names, "WIP full package became a dependency prematurely")

    check(not (ROOT / "linspectacles-applets/packaging").exists(), "WIP applets package unexpectedly has packaging source")
    check(not (ROOT / "linspectacles-full/packaging").exists(), "WIP full package unexpectedly has packaging source")
    check("Work in progress" in applets, "applets placeholder is not marked WIP")
    check("Work in progress" in full, "full placeholder is not marked WIP")

    check("%{_bindir}" not in spec and "/usr/bin/linspectacles" not in spec, "metapackage attempts to own a launcher")
    check("%{_datadir}/applications" not in spec, "metapackage attempts to own a desktop entry")
    check("%doc README.md" in spec and "%license LICENSE" in spec, "spec documentation/licence file list changed")

    check(BUILD.stat().st_mode & 0o111 != 0, "RPM build script is not executable")
    result = subprocess.run(["bash", "-n", str(BUILD)], capture_output=True, text=True)
    check(result.returncode == 0, f"Bash syntax error: {result.stderr.strip()}")

    check(HUB in rpm_readme and MODULES in rpm_readme, "RPM README omits required dependencies")

    with tempfile.TemporaryDirectory(prefix="linspectacles-metapackages-qa-") as tmp:
        out = Path(tmp) / "out"
        env = dict(os.environ, RPM_OUTPUT_DIR=str(out))
        result = subprocess.run([str(BUILD), "--prepare-only"], capture_output=True, text=True, env=env)
        check(result.returncode == 0, f"prepare-only failed: {result.stderr.strip()}")
        tarball = out / "linspectacles-0.0.2.tar.gz"
        generated_spec = out / "linspectacles.spec"
        check(tarball.is_file(), "prepare-only did not create 0.0.2 source tarball")
        check(generated_spec.is_file(), "prepare-only did not create generated spec")
        if tarball.is_file():
            try:
                with tarfile.open(tarball, "r:gz") as tf:
                    names = sorted(tf.getnames())
                check(names == [
                    "linspectacles-0.0.2",
                    "linspectacles-0.0.2/LICENSE",
                    "linspectacles-0.0.2/README.md",
                ], f"unexpected source tarball contents: {names}")
            except (tarfile.TarError, OSError) as exc:
                errors.append(f"source tarball could not be read: {exc}")

    if errors:
        for item in errors:
            print(f"FAIL: {item}", file=sys.stderr)
        return 1

    print("PASS: linspectacles-metapackages 0.0.2 layout, exact linspectacles dependency contract, WIP sibling boundaries, shell syntax, source generation")
    return 0


if __name__ == "__main__":
    sys.exit(validate())
