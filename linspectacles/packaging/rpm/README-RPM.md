# RPM packaging — linspectacles

This directory contains the Fedora/RPM packaging source for the dependency-only **`linspectacles`** metapackage.

Current metapackage release: **0.0.3**

Canonical source repository: <https://github.com/linspectacles/linspectacles-metapackages>

## Dependency contract

The package dependency contract is:

```spec
Requires:       linspectacles-hub
Recommends:     linspectacles-modules
```

There are deliberately no exact dependency-version pins. Standard DNF installations include the recommended Modules metapackage by default, while allowing it to be removed independently from `linspectacles` and the required Hub package.

The package contains no Hub source, Module source, applet source, launcher, desktop entry, helper, or other runtime payload. Those remain owned by their individual packages and repositories.

The future `linspectacles-applets` and `linspectacles-full` metapackages are **not** dependencies of `linspectacles`.

## Prepare RPM inputs

From the repository root:

```bash
./linspectacles/packaging/rpm/build-rpm-fedora.sh --prepare-only
```

This creates:

```text
linspectacles/packaging/rpm/dist-rpm/
├── linspectacles-0.0.3.tar.gz
└── linspectacles.spec
```

The source tarball contains only the documentation and license payload needed by this dependency-only RPM:

```text
linspectacles-0.0.3/
├── LICENSE
└── README.md
```

## Build RPM and SRPM

On Fedora:

```bash
sudo dnf install rpm-build
./linspectacles/packaging/rpm/build-rpm-fedora.sh
```

Binary RPM and SRPM output is copied into `dist-rpm/` together with the prepared source tarball and spec.

## Ownership boundary

Installing `linspectacles` composes the core LinSpectacles workbench by requiring `linspectacles-hub` and recommending `linspectacles-modules`. It does not duplicate or take ownership of files from either dependency.
