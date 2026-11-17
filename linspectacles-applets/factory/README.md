# LinSpectacles Applet RPM Factory 0.0.4

The Applet RPM Factory turns a directory or ZIP containing LinSpectacles applet source trees into RPM build inputs and, when requested, SRPMs suitable for COPR.

It is deliberately catalog-less. Every applet is discovered from its own `applet.json` and must satisfy the common LinSpectacles source contract.

## Stages

1. **Discover and validate** — find applets, validate required metadata/files, verify privileged-helper hashes when declared.
2. **Prepare** — create one clean source tarball and generated RPM spec per applet. `__pycache__`, `*.pyc`, `*.pyo`, VCS metadata and build output are excluded.
3. **Build SRPMs** — optional; runs `rpmbuild -bs` locally and collects successful SRPMs under `dist/srpm/`.
4. **Submit to COPR** — optional and opt-in; submits built SRPMs with `copr-cli build ... --nowait`. Existing SRPMs can also be submitted directly later without repeating discovery, preparation or build.

The default mode is interactive but concise. It pauses before each stage that creates build output or submits anything. COPR submission defaults to **No**.

## Requirements

For discovery and preparation:

- Python 3

For local SRPM building:

```bash
sudo dnf install rpm-build
```

For optional COPR submission:

```bash
sudo dnf install copr-cli
```

Configure COPR authentication in `~/.config/copr` before using the submit stage.

## Typical use

With a directory containing applet roots:

```bash
python3 factory/factory.py /path/to/applets
```

With a ZIP containing applet roots:

```bash
python3 factory/factory.py /path/to/linspectacles_applets.zip
```

The factory reports the discovered count, validates all applets, and then asks whether to continue through Prepare, Build and Submit.

## Useful controls

Prepare only without prompts:

```bash
python3 factory/factory.py /path/to/applets --through prepare --non-interactive
```

Build SRPMs without COPR submission:

```bash
python3 factory/factory.py /path/to/applets --through build --non-interactive
```

Select one or more applets by glob:

```bash
python3 factory/factory.py /path/to/applets --only 'linspectacles-gpu-*' --only 'linspectacles-tpm-*'
```

Submit already-built SRPMs during a full run:

```bash
python3 factory/factory.py /path/to/applets \
  --through submit \
  --copr-project brunonlinespace/linspectacles
```

Without `--non-interactive`, the factory still asks before COPR submission.

Submit an already-built SRPM directory without rebuilding anything:

```bash
python3 factory/factory.py --submit-existing dist/srpm
```

The factory shows the number of SRPMs and target COPR project, then asks once before submitting the batch. COPR submission still defaults to **No**.

To submit an already-reviewed batch without the confirmation prompt:

```bash
python3 factory/factory.py \
  --submit-existing dist/srpm \
  --copr-project brunonlinespace/linspectacles \
  --non-interactive
```

`--only` can be combined with `--submit-existing` to restrict the batch by filename glob.

## Generated RPM policy

Each applet RPM:

- uses `applet.json.id` as the RPM package name;
- uses `applet.json.version` as the RPM version;
- uses `applet.json.repository` as the RPM URL;
- installs the complete clean applet tree into `/usr/libexec/linspectacles/applets/<python-root>/`, the Hub's package-managed applet store;
- remains independently runnable through `/usr/bin/<applet-id>`;
- does **not** require `linspectacles-hub`;
- requires Python 3 and PyQt6;
- converts declared `python_dependencies` entries to `python3dist(...)` RPM requirements;
- accepts optional applet-local `rpm_requires` entries for genuine hard RPM dependencies without creating a central catalogue;
- installs a declared privileged-helper payload at its manifest `install_path` and adds a `polkit` dependency;
- adds a second `-tui` launcher when `standalone_tui` is declared.

The factory does not infer system-command dependencies from source code. Missing optional Linux tools remain governed by each applet's existing availability/error handling. If a future applet needs a hard packaging dependency beyond the common Python requirements, it can declare `rpm_requires` in its own metadata rather than adding an applet-specific central catalogue.

## Output

```text
dist/
├── prepared/
│   └── <rpm-name>/
│       ├── <rpm-name>.spec
│       └── <rpm-name>-<version>.tar.gz
├── srpm/
└── logs/
```

One applet failure does not hide the rest: the factory continues and prints a final PASS/FAIL summary. The Submit stage is offered only for SRPMs that built successfully.
