# Changelog

## 0.0.4

- Makes COPR batch submission visibly progressive instead of appearing frozen while sequential `copr-cli` calls run.
- Prints the package being submitted and its immediate success/failure before moving to the next SRPM.
- No RPM preparation, build, dependency, or COPR target behavior changed.

## 0.0.3 — 2026-11-16

- Corrects the COPR submission flag from `--no-wait` to the `copr-cli` form `--nowait`.
- No other factory behavior changes.

## 0.0.2 — 2026-11-16

- Adds independent submission of already-built SRPMs with `--submit-existing SRPM_DIR`.
- Existing-SRPM submission skips discovery, preparation and `rpmbuild` completely.
- Shows the discovered SRPM count and COPR target before publication and asks once; submission remains opt-in by default.
- Supports `--only` filtering and optional `--non-interactive` operation for reviewed batches.
- Preserves the 0.0.1 discovery, preparation, build and full-pipeline behavior unchanged.

## 0.0.1 — 2026-11-16

- First catalog-less LinSpectacles applet RPM factory.
- Discovers applets from `applet.json` in directories or ZIP collections.
- Validates canonical root files, entrypoints, Linux platform declaration and privileged-helper hashes.
- Generates clean per-applet source tarballs and RPM specs without cache artefacts.
- Installs RPM applets into the Hub package-managed store at `/usr/libexec/linspectacles/applets/` while preserving standalone launchers.
- Supports manifest-declared Python dependencies, privileged helper installation and optional TUI launchers.
- Adds staged interactive operation: Discover/Validate → Prepare → Build SRPMs → optional COPR Submit.
- Adds non-interactive `--through` mode and glob selection for later automation.
