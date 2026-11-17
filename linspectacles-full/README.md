# LinSpectacles Full — RPM metapackage

`linspectacles-full` is the dependency-only RPM metapackage for installing the complete LinSpectacles environment: the Hub and recommended Hub Modules through `linspectacles`, plus the complete official applet collection through `linspectacles-applets`.

Current metapackage release: **0.0.1**

Repository: <https://github.com/linspectacles/linspectacles-metapackages>

## Dependency model

The metapackage contains no application, applet, module, helper, or runtime payload of its own. It requires exactly two sibling metapackages:

```text
Requires: linspectacles
Requires: linspectacles-applets
```

There are deliberately no exact version pins.

The dependency hierarchy is therefore:

```text
linspectacles-full
├── linspectacles
│   ├── linspectacles-hub                    (required)
│   └── linspectacles-modules                (recommended)
└── linspectacles-applets                    (required)
    └── all official LinSpectacles applets   (recommended)
```

The lower-level metapackages remain authoritative for their own dependency policy. `linspectacles-full` does not duplicate the Hub, Modules, or individual applet dependency lists.

## Installation

After publication to the configured repository:

```bash
sudo dnf install linspectacles-full
```

With normal DNF weak-dependency behavior enabled, this installs the Hub, the recommended Hub Modules set, `linspectacles-applets`, and its recommended official applet collection.

## Removal behavior

Because `linspectacles-full` hard-requires both sibling metapackages, removing either `linspectacles` or `linspectacles-applets` makes `linspectacles-full` no longer satisfiable and DNF may include it in the removal transaction.

Individual applets remain independently removable because they are weak dependencies of `linspectacles-applets`, not direct dependencies of `linspectacles-full`.

When `linspectacles-full` itself is removed with DNF's normal `clean_requirements_on_remove` behavior enabled, packages installed solely as dependencies of it and no longer needed may become eligible for cleanup. Explicitly user-installed packages may remain.

## RPM build

The RPM source and builder are under [`packaging/rpm/`](packaging/rpm/).

Build the binary RPM and SRPM on Fedora with:

```bash
cd linspectacles-full/packaging/rpm
./build-rpm-fedora.sh
```

Or prepare only the spec and source tarball:

```bash
./build-rpm-fedora.sh --prepare-only
```

Generated artifacts are written to `packaging/rpm/dist-rpm/`.

## License

GNU General Public License v3.0 or later. See [`../LICENSE`](../LICENSE).
