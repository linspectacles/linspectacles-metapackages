#!/usr/bin/env python3
"""LinSpectacles catalog-less applet RPM factory."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

FACTORY_VERSION = "0.0.4"
DEFAULT_COPR_PROJECT = "brunonlinespace/linspectacles"
SYSTEM_APPLET_ROOT = "/usr/libexec/linspectacles/applets"
REQUIRED_ROOT_FILES = ("__init__.py", "standalone.py", "README.md", "LICENSE", "applet.json")
REQUIRED_MANIFEST_KEYS = (
    "schema",
    "id",
    "name",
    "version",
    "repository",
    "entrypoint",
    "standalone",
    "description",
    "platforms",
)
SKIP_DIRS = {"__pycache__", ".git", ".hg", ".svn", "dist", "build", ".pytest_cache", ".mypy_cache"}
SKIP_SUFFIXES = {".pyc", ".pyo"}
RPM_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9+._-]*$")
VERSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+~]*$")


@dataclass
class Applet:
    root: Path
    manifest: dict
    rpm_name: str
    version: str
    display_name: str
    python_root: str
    repository: str
    description: str
    standalone: str
    standalone_tui: str | None = None
    python_dependencies: list[str] = field(default_factory=list)
    rpm_requires: list[str] = field(default_factory=list)
    privileged_helper: dict | None = None


@dataclass
class Result:
    name: str
    ok: bool
    detail: str = ""
    path: Path | None = None


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def yes_no(prompt: str, default: bool) -> bool:
    suffix = " [Y/n] " if default else " [y/N] "
    while True:
        answer = input(prompt + suffix).strip().lower()
        if not answer:
            return default
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please answer y or n.")


def run(cmd: list[str], *, cwd: Path | None = None, log: Path | None = None) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if log:
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text(proc.stdout or "", encoding="utf-8")
    return proc


def source_root(path: Path, temp_stack: list[tempfile.TemporaryDirectory]) -> Path:
    path = path.expanduser().resolve()
    if not path.exists():
        raise ValueError(f"Source path does not exist: {path}")
    if path.is_dir():
        return path
    if path.is_file() and path.suffix.lower() == ".zip":
        td = tempfile.TemporaryDirectory(prefix="linspectacles-applet-factory-")
        temp_stack.append(td)
        shutil.unpack_archive(str(path), td.name)
        return Path(td.name)
    raise ValueError("Source must be a directory or .zip archive.")


def candidate_roots(root: Path) -> list[Path]:
    if (root / "applet.json").is_file():
        return [root]
    direct = sorted(p for p in root.iterdir() if p.is_dir() and (p / "applet.json").is_file())
    if direct:
        return direct
    # Allow one wrapper directory around the collection.
    children = [p for p in root.iterdir() if p.is_dir()]
    if len(children) == 1:
        wrapper = children[0]
        return sorted(p for p in wrapper.iterdir() if p.is_dir() and (p / "applet.json").is_file())
    return []


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_applet(root: Path) -> Applet:
    missing = [name for name in REQUIRED_ROOT_FILES if not (root / name).is_file()]
    if missing:
        raise ValueError("missing root file(s): " + ", ".join(missing))

    try:
        manifest = json.loads((root / "applet.json").read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"invalid applet.json: {exc}") from exc

    missing_keys = [key for key in REQUIRED_MANIFEST_KEYS if key not in manifest]
    if missing_keys:
        raise ValueError("missing manifest key(s): " + ", ".join(missing_keys))
    if manifest.get("schema") != 1:
        raise ValueError(f"unsupported applet.json schema: {manifest.get('schema')!r}")

    rpm_name = str(manifest["id"]).strip()
    if not RPM_NAME_RE.fullmatch(rpm_name):
        raise ValueError(f"invalid RPM/applet id: {rpm_name!r}")
    if not rpm_name.startswith("linspectacles-"):
        raise ValueError(f"applet id must start with 'linspectacles-': {rpm_name}")

    version = str(manifest["version"]).strip()
    if not VERSION_RE.fullmatch(version):
        raise ValueError(f"unsupported RPM version syntax: {version!r}")

    python_root = root.name
    if not python_root.isidentifier():
        raise ValueError(f"source root must be a Python identifier: {python_root!r}")

    entrypoint = root / str(manifest["entrypoint"])
    standalone = root / str(manifest["standalone"])
    if not entrypoint.is_file():
        raise ValueError(f"entrypoint missing: {manifest['entrypoint']}")
    if not standalone.is_file():
        raise ValueError(f"standalone launcher missing: {manifest['standalone']}")

    platforms = manifest.get("platforms")
    if not isinstance(platforms, list) or "linux" not in platforms:
        raise ValueError("factory currently packages Linux applets only")

    repository = str(manifest["repository"]).strip()
    if not repository.startswith(("https://", "http://")):
        raise ValueError(f"repository must be an HTTP(S) URL: {repository!r}")

    python_dependencies = manifest.get("python_dependencies", [])
    if not isinstance(python_dependencies, list) or not all(isinstance(x, str) and x.strip() for x in python_dependencies):
        raise ValueError("python_dependencies must be a list of non-empty strings")
    for dep in python_dependencies:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", dep.strip()):
            raise ValueError(f"python_dependencies entries must be distribution names only: {dep!r}")

    rpm_requires = manifest.get("rpm_requires", [])
    if not isinstance(rpm_requires, list) or not all(isinstance(x, str) and x.strip() and "\n" not in x and "\r" not in x for x in rpm_requires):
        raise ValueError("rpm_requires must be a list of non-empty single-line RPM dependency expressions")

    standalone_tui = manifest.get("standalone_tui")
    if standalone_tui is not None:
        tui_path = root / str(standalone_tui)
        if not tui_path.is_file():
            raise ValueError(f"standalone_tui launcher missing: {standalone_tui}")
        standalone_tui = str(standalone_tui)

    helper = manifest.get("privileged_helper")
    if helper is not None:
        if not isinstance(helper, dict):
            raise ValueError("privileged_helper must be an object")
        for key in ("payload", "install_path", "sha256"):
            if not helper.get(key):
                raise ValueError(f"privileged_helper missing {key}")
        payload = root / str(helper["payload"])
        if not payload.is_file():
            raise ValueError(f"privileged helper payload missing: {helper['payload']}")
        install_path = str(helper["install_path"])
        if not install_path.startswith("/usr/libexec/"):
            raise ValueError(f"privileged helper install_path must be under /usr/libexec: {install_path}")
        actual = sha256(payload)
        expected = str(helper["sha256"]).lower()
        if actual != expected:
            raise ValueError(f"privileged helper SHA-256 mismatch: expected {expected}, got {actual}")

    return Applet(
        root=root,
        manifest=manifest,
        rpm_name=rpm_name,
        version=version,
        display_name=str(manifest["name"]).strip(),
        python_root=python_root,
        repository=repository,
        description=str(manifest["description"]).strip(),
        standalone=str(manifest["standalone"]),
        standalone_tui=standalone_tui,
        python_dependencies=[x.strip() for x in python_dependencies],
        rpm_requires=[x.strip() for x in rpm_requires],
        privileged_helper=helper,
    )


def discover(root: Path, patterns: list[str]) -> tuple[list[Applet], list[Result]]:
    roots = candidate_roots(root)
    if not roots:
        return [], [Result("source", False, "no applet.json roots discovered")]

    applets: list[Applet] = []
    results: list[Result] = []
    seen_names: set[str] = set()
    for candidate in roots:
        try:
            applet = validate_applet(candidate)
            if patterns and not any(fnmatch.fnmatch(applet.rpm_name, pattern) or fnmatch.fnmatch(candidate.name, pattern) for pattern in patterns):
                continue
            if applet.rpm_name in seen_names:
                raise ValueError(f"duplicate applet/RPM id: {applet.rpm_name}")
            seen_names.add(applet.rpm_name)
            applets.append(applet)
            results.append(Result(applet.rpm_name, True, f"{applet.version} — {applet.display_name}"))
        except Exception as exc:
            results.append(Result(candidate.name, False, str(exc)))
    return applets, results


def should_skip(rel: Path) -> bool:
    if any(part in SKIP_DIRS for part in rel.parts):
        return True
    if rel.suffix in SKIP_SUFFIXES:
        return True
    return False


def clean_copy(src: Path, dst: Path) -> None:
    for path in src.rglob("*"):
        rel = path.relative_to(src)
        if should_skip(rel):
            continue
        target = dst / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif path.is_symlink():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(os.readlink(path))
        elif path.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def rpm_escape(text: str) -> str:
    return text.replace("%", "%%")


def summary_for(applet: Applet) -> str:
    text = " ".join(applet.description.split())
    first = re.split(r"(?<=[.!?])\s+", text, maxsplit=1)[0]
    first = first.rstrip(".")
    if len(first) > 110:
        first = first[:107].rstrip() + "..."
    return rpm_escape(first or f"LinSpectacles applet: {applet.display_name}")


def description_for(applet: Applet) -> str:
    text = " ".join(applet.description.split())
    return rpm_escape(text)


def render_spec(applet: Applet, template: str) -> str:
    extra_requires = []
    for dep in sorted(set(applet.python_dependencies)):
        extra_requires.append(f"Requires:       python3dist({dep})")
    for dep in applet.rpm_requires:
        extra_requires.append(f"Requires:       {dep}")
    if applet.privileged_helper:
        extra_requires.append("Requires:       polkit")

    tui_install = ""
    tui_files = ""
    if applet.standalone_tui:
        tui_install = f'''cat > "%{{buildroot}}%{{_bindir}}/%{{name}}-tui" <<'APPLET_TUI_LAUNCHER'\n#!/bin/sh\nexec /usr/bin/python3 "%{{_libexecdir}}/linspectacles/applets/{applet.python_root}/{applet.standalone_tui}" "$@"\nAPPLET_TUI_LAUNCHER\nchmod 0755 "%{{buildroot}}%{{_bindir}}/%{{name}}-tui"'''
        tui_files = "%{_bindir}/%{name}-tui"

    helper_install = ""
    helper_files = ""
    if applet.privileged_helper:
        payload = str(applet.privileged_helper["payload"])
        install_path = str(applet.privileged_helper["install_path"])
        helper_install = f'install -Dm0755 "{payload}" "%{{buildroot}}{install_path}"'
        helper_files = install_path

    replacements = {
        "@NAME@": applet.rpm_name,
        "@VERSION@": applet.version,
        "@SUMMARY@": summary_for(applet),
        "@URL@": applet.repository,
        "@DESCRIPTION@": description_for(applet),
        "@PYTHON_ROOT@": applet.python_root,
        "@STANDALONE@": applet.standalone,
        "@DISPLAY_NAME@": rpm_escape(applet.display_name),
        "@EXTRA_REQUIRES@": "\n".join(extra_requires),
        "@TUI_INSTALL@": tui_install,
        "@TUI_FILES@": tui_files,
        "@HELPER_INSTALL@": helper_install,
        "@HELPER_FILES@": helper_files,
    }
    out = template
    for needle, value in replacements.items():
        out = out.replace(needle, value)
    return out


def prepare_one(applet: Applet, prepared_root: Path, template: str) -> Result:
    package_dir = prepared_root / applet.rpm_name
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True)

    top_name = f"{applet.rpm_name}-{applet.version}"
    tar_path = package_dir / f"{top_name}.tar.gz"
    spec_path = package_dir / f"{applet.rpm_name}.spec"

    with tempfile.TemporaryDirectory(prefix="linspectacles-applet-source-") as td:
        staged = Path(td) / top_name
        staged.mkdir()
        clean_copy(applet.root, staged)
        with tarfile.open(tar_path, "w:gz") as tf:
            tf.add(staged, arcname=top_name)

    spec_path.write_text(render_spec(applet, template), encoding="utf-8")

    # Guard the central promise: generated source archives carry no caches.
    with tarfile.open(tar_path, "r:gz") as tf:
        bad = [m.name for m in tf.getmembers() if "__pycache__" in Path(m.name).parts or Path(m.name).suffix in SKIP_SUFFIXES]
    if bad:
        return Result(applet.rpm_name, False, f"cache artefacts leaked into source archive: {bad[0]}")

    return Result(applet.rpm_name, True, f"prepared {applet.version}", package_dir)


def build_one(applet: Applet, prepared_dir: Path, srpm_root: Path, logs_root: Path) -> Result:
    spec = prepared_dir / f"{applet.rpm_name}.spec"
    source = prepared_dir / f"{applet.rpm_name}-{applet.version}.tar.gz"
    with tempfile.TemporaryDirectory(prefix="linspectacles-rpmbuild-") as td:
        top = Path(td)
        for name in ("BUILD", "BUILDROOT", "RPMS", "SOURCES", "SPECS", "SRPMS"):
            (top / name).mkdir()
        shutil.copy2(spec, top / "SPECS" / spec.name)
        shutil.copy2(source, top / "SOURCES" / source.name)
        log = logs_root / f"{applet.rpm_name}-rpmbuild.log"
        proc = run(["rpmbuild", "-bs", "--define", f"_topdir {top}", str(top / "SPECS" / spec.name)], log=log)
        if proc.returncode != 0:
            return Result(applet.rpm_name, False, f"rpmbuild failed; see {log}")
        built = sorted((top / "SRPMS").glob("*.src.rpm"))
        if len(built) != 1:
            return Result(applet.rpm_name, False, f"expected one SRPM, found {len(built)}")
        srpm_root.mkdir(parents=True, exist_ok=True)
        dest = srpm_root / built[0].name
        shutil.copy2(built[0], dest)
        return Result(applet.rpm_name, True, dest.name, dest)


def submit_one(srpm: Path, project: str, logs_root: Path) -> Result:
    log = logs_root / f"{srpm.stem}-copr.log"
    proc = run(["copr-cli", "build", project, "--nowait", str(srpm)], log=log)
    if proc.returncode != 0:
        return Result(srpm.name, False, f"COPR submission failed; see {log}")
    detail = "submitted"
    output = (proc.stdout or "").strip()
    if output:
        last = output.splitlines()[-1].strip()
        detail = f"submitted — {last}"
    return Result(srpm.name, True, detail, srpm)


def existing_srpms(root: Path, patterns: list[str]) -> list[Path]:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"SRPM directory does not exist: {root}")
    srpms = sorted(root.glob("*.src.rpm"))
    if patterns:
        srpms = [
            p for p in srpms
            if any(fnmatch.fnmatch(p.name, pattern) or fnmatch.fnmatch(p.name.removesuffix(".src.rpm"), pattern) for pattern in patterns)
        ]
    return srpms


def submit_existing_mode(args: argparse.Namespace) -> int:
    try:
        srpms = existing_srpms(Path(args.submit_existing), args.only)
    except ValueError as exc:
        eprint(f"error: {exc}")
        return 2

    if not srpms:
        eprint("error: no matching .src.rpm files found")
        return 1

    project = args.copr_project
    print(f"Existing SRPMs: {len(srpms)}")
    print(f"COPR target: {project}")
    if args.verbose:
        for srpm in srpms:
            print(f"  {srpm.name}")

    if not shutil.which("copr-cli"):
        eprint("error: copr-cli not found. Install it with: sudo dnf install copr-cli")
        return 2

    if not args.non_interactive:
        if not yes_no(f"Submit {len(srpms)} existing SRPM(s) to {project}?", False):
            print("No SRPMs submitted.")
            return 0

    logs_root = Path(args.output).expanduser().resolve() / "logs"
    results = []
    total = len(srpms)
    for index, srpm in enumerate(srpms, start=1):
        print(f"[{index}/{total}] Submitting {srpm.name} ...", flush=True)
        result = submit_one(srpm, project, logs_root)
        results.append(result)
        status = "OK" if result.ok else "FAIL"
        print(f"[{index}/{total}] {status}: {result.detail}", flush=True)

    _, failed = print_results("COPR submission", results, True)
    if failed:
        return 1
    print(f"Submitted {len(results)} build(s) to {project}.")
    return 0


def print_results(title: str, results: Iterable[Result], verbose: bool = False) -> tuple[int, int]:
    results = list(results)
    ok = sum(1 for r in results if r.ok)
    failed = len(results) - ok
    print(f"\n{title}: {ok} passed", end="")
    if failed:
        print(f", {failed} failed")
    else:
        print()
    if verbose or failed:
        for r in results:
            if verbose or not r.ok:
                marker = "PASS" if r.ok else "FAIL"
                detail = f" — {r.detail}" if r.detail else ""
                print(f"  [{marker}] {r.name}{detail}")
    return ok, failed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=f"LinSpectacles Applet RPM Factory {FACTORY_VERSION}")
    parser.add_argument("source", nargs="?", help="directory or ZIP containing applet source roots")
    parser.add_argument("--submit-existing", metavar="SRPM_DIR",
                        help="submit existing *.src.rpm files from SRPM_DIR without discovery, preparation or rebuilding")
    parser.add_argument("--output", default="dist", help="output directory (default: ./dist)")
    parser.add_argument("--through", choices=("discover", "prepare", "build", "submit"), default=None,
                        help="run automatically through this stage; interactive mode asks between stages")
    parser.add_argument("--non-interactive", action="store_true", help="do not prompt; requires --through or --submit-existing")
    parser.add_argument("--only", action="append", default=[], metavar="GLOB",
                        help="include only applet/RPM names matching GLOB; may be repeated")
    parser.add_argument("--copr-project", default=DEFAULT_COPR_PROJECT,
                        help=f"COPR target for submit stage (default: {DEFAULT_COPR_PROJECT})")
    parser.add_argument("--verbose", action="store_true", help="print per-applet PASS lines")
    parser.add_argument("--version", action="version", version=f"%(prog)s {FACTORY_VERSION}")
    args = parser.parse_args()
    if args.submit_existing and args.through:
        parser.error("--submit-existing cannot be combined with --through")
    if args.submit_existing and args.source:
        parser.error("source cannot be supplied with --submit-existing")
    if args.non_interactive and not (args.through or args.submit_existing):
        parser.error("--non-interactive requires --through or --submit-existing")
    return args


def main() -> int:
    args = parse_args()
    print(f"LinSpectacles Applet RPM Factory {FACTORY_VERSION}")

    if args.submit_existing:
        return submit_existing_mode(args)

    source_arg = args.source
    if not source_arg:
        if args.non_interactive:
            eprint("error: source path is required in non-interactive mode")
            return 2
        source_arg = input("Applet source directory or ZIP: ").strip()
        if not source_arg:
            eprint("No source selected.")
            return 2

    temp_stack: list[tempfile.TemporaryDirectory] = []
    try:
        root = source_root(Path(source_arg), temp_stack)
        applets, validation = discover(root, args.only)
        _, failed = print_results("Discovery/validation", validation, args.verbose)
        if failed:
            print("Validation failures must be fixed before packaging; no later stages were run.")
            return 1
        if not applets:
            print("No applets matched the requested selection.")
            return 1
        print(f"Selected: {len(applets)} applet(s)")

        stages = {"discover": 0, "prepare": 1, "build": 2, "submit": 3}
        if args.through:
            target_stage = stages[args.through]
        else:
            target_stage = None

        if target_stage == 0:
            return 0

        output = Path(args.output).expanduser().resolve()
        prepared_root = output / "prepared"
        srpm_root = output / "srpm"
        logs_root = output / "logs"
        template_path = Path(__file__).resolve().parent / "templates" / "applet.spec.tpl"
        template = template_path.read_text(encoding="utf-8")

        do_prepare = target_stage is not None and target_stage >= 1
        if target_stage is None:
            do_prepare = yes_no(f"Prepare RPM inputs for {len(applets)} applet(s)?", True)
        if not do_prepare:
            print("Stopped after validation.")
            return 0

        prepare_results = [prepare_one(a, prepared_root, template) for a in applets]
        _, prep_failed = print_results("Prepare", prepare_results, args.verbose)
        if prep_failed:
            print("Preparation had failures; Build/Submit stages were not run.")
            return 1
        print(f"Prepared inputs: {prepared_root}")

        if target_stage == 1:
            return 0

        do_build = target_stage is not None and target_stage >= 2
        if target_stage is None:
            if shutil.which("rpmbuild"):
                do_build = yes_no(f"Build {len(applets)} SRPM(s) now?", True)
            else:
                print("rpmbuild is not installed; stopping after Prepare. Install it with: sudo dnf install rpm-build")
                return 0
        if not do_build:
            print("Stopped after Prepare.")
            return 0
        if not shutil.which("rpmbuild"):
            eprint("error: rpmbuild not found. Install it with: sudo dnf install rpm-build")
            return 2

        build_results = []
        for applet in applets:
            build_results.append(build_one(applet, prepared_root / applet.rpm_name, srpm_root, logs_root))
        _, build_failed = print_results("SRPM build", build_results, args.verbose)
        print(f"SRPM output: {srpm_root}")
        if build_failed:
            print("Some SRPMs failed. Successful SRPMs were kept; Submit was not offered for this release set.")
            return 1

        if target_stage == 2:
            return 0

        do_submit = target_stage is not None and target_stage >= 3
        project = args.copr_project
        if target_stage is None:
            do_submit = yes_no(f"Submit {len(build_results)} SRPM(s) to COPR?", False)
            if do_submit:
                entered = input(f"COPR project [{project}]: ").strip()
                if entered:
                    project = entered
        elif not args.non_interactive:
            if not yes_no(f"Submit {len(build_results)} SRPM(s) to COPR project {project}?", False):
                print("Stopped after SRPM build.")
                return 0

        if not do_submit:
            print("Stopped after SRPM build.")
            return 0
        if not shutil.which("copr-cli"):
            eprint("error: copr-cli not found. Install it with: sudo dnf install copr-cli")
            return 2

        submit_candidates = [r.path for r in build_results if r.path]
        submit_results = []
        total = len(submit_candidates)
        for index, srpm in enumerate(submit_candidates, start=1):
            print(f"[{index}/{total}] Submitting {srpm.name} ...", flush=True)
            result = submit_one(srpm, project, logs_root)
            submit_results.append(result)
            status = "OK" if result.ok else "FAIL"
            print(f"[{index}/{total}] {status}: {result.detail}", flush=True)

        _, submit_failed = print_results("COPR submission", submit_results, True)
        if submit_failed:
            return 1
        print(f"Submitted {len(submit_results)} build(s) to {project}.")
        return 0
    finally:
        for td in temp_stack:
            td.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
