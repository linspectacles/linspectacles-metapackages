# Factory 0.0.1 QA

Validated against the supplied LinSpectacles applet collection on 2026-11-16.

- 43 applet roots discovered from `applet.json`.
- 43/43 passed structural and manifest validation.
- 6/6 declared privileged-helper payloads matched their manifest SHA-256 values.
- 43/43 RPM specs generated.
- 43/43 clean source tarballs generated.
- Generated tarballs contain no `__pycache__`, `*.pyc` or `*.pyo` artefacts.
- Resource Monitor correctly generated its `python3dist(psutil)` requirement, privileged-helper installation and additional TUI launcher.
- Applets declaring privileged helpers correctly generated a `polkit` requirement and fixed `/usr/libexec/...` helper installation.

The execution environment used for this QA does not provide `rpmbuild` or `copr-cli`, so the local SRPM-build and COPR-submit stages were not executed here. Both stages perform explicit executable checks before running.

## 0.0.2 existing-SRPM submission

- `--submit-existing` does not require an applet source path.
- It accepts only an existing directory and scans only top-level `*.src.rpm` files.
- `--through` and a source argument are rejected when `--submit-existing` is active.
- Interactive submission asks once and defaults to No.
- `--non-interactive` is permitted with `--submit-existing`.
- `--only` filtering remains available for an existing SRPM batch.
- No discovery, Prepare or Build stage is entered in existing-SRPM mode.
