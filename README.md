# LinSpectacles Metapackages

**Dependency-only RPM metapackages for composing LinSpectacles installation sets.**

Current repository release: **0.0.5**

Repository: <https://github.com/linspectacles/linspectacles-metapackages>

## What this repository is

`linspectacles-metapackages` is the source repository for the small dependency-only RPM packages that compose larger LinSpectacles installation sets.

It does **not** duplicate the Hub, Hub Modules, or inspector applet sources. Those remain in their own repositories and continue to own their own runtime files and RPM packaging.

The metapackages here only express installation relationships between those independently packaged components.

## Metapackage family

| Metapackage | Composition | Status |
| --- | --- | --- |
| **`linspectacles`** | requires `linspectacles-hub`; recommends `linspectacles-modules` | **Available — 0.0.3** |
| **`linspectacles-applets`** | recommends all 44 official LinSpectacles applet RPMs | **Available — 0.0.1** |
| **`linspectacles-full`** | requires `linspectacles` + `linspectacles-applets` | **Available — 0.0.1** |

The intended package relationship is:

```text
linspectacles-full
├── linspectacles
│   ├── linspectacles-hub
│   └── linspectacles-modules (recommended)
└── linspectacles-applets
    └── all 44 official LinSpectacles applet RPMs (recommended)
```

**`linspectacles`**, **`linspectacles-applets`**, and **`linspectacles-full`** are implemented in this repository release.

## Repository layout

```text
linspectacles-metapackages/
├── .github/
│   └── REPOSITORY-ABOUT.md
├── linspectacles/
│   ├── README.md
│   └── packaging/
│       └── rpm/
│           ├── README-RPM.md
│           ├── build-rpm-fedora.sh
│           └── linspectacles.spec
├── linspectacles-applets/
│   ├── README.md
│   ├── factory/
│   │   └── ...
│   └── packaging/
│       └── rpm/
│           ├── README-RPM.md
│           ├── build-rpm-fedora.sh
│           └── linspectacles-applets.spec
├── linspectacles-full/
│   ├── README.md
│   └── packaging/
│       └── rpm/
│           ├── README-RPM.md
│           ├── build-rpm-fedora.sh
│           └── linspectacles-full.spec
├── .gitignore
├── LICENSE
└── README.md
```

This layout is intentional: each metapackage occupies a sibling directory, while repository-wide documentation and licensing remain at the repository root.

## Implemented metapackage: linspectacles

The currently implemented metapackage requires the Hub and recommends the optional Hub Modules metapackage:

```text
Requires:   linspectacles-hub
Recommends: linspectacles-modules
```

Standard DNF installations include recommended dependencies by default. The package has no runtime payload of its own and deliberately has no exact dependency-version pins.

See [`linspectacles/README.md`](linspectacles/README.md) for the package contract and build instructions.

## Implemented metapackage: linspectacles-applets

The applet collection metapackage recommends all 44 official applet RPMs without exact version pins. Standard DNF installations therefore pull in the complete applet set by default, while any individual applet can be removed without forcing removal of the metapackage or the rest of the collection.

`linspectacles-applets` has no dependency on the Hub, Hub Modules, or the top-level `linspectacles` metapackage. See [`linspectacles-applets/README.md`](linspectacles-applets/README.md) for the complete dependency list and removal semantics.

## Implemented metapackage: linspectacles-full

The complete-installation metapackage requires the two sibling composition packages:

```text
Requires: linspectacles
Requires: linspectacles-applets
```

It does not duplicate the Hub, Modules, or 44-applet dependency lists. Those policies remain owned by `linspectacles` and `linspectacles-applets`. See [`linspectacles-full/README.md`](linspectacles-full/README.md) for the package contract and build instructions.

## Existing dependency repositories

The dependencies remain separately developed and packaged:

- LinSpectacles Hub: <https://github.com/linspectacles/linspectacles-hub>
- LinSpectacles Hub Modules: <https://github.com/linspectacles/linspectacles-modules>

Nothing from either repository is vendored into this metapackage repository.

## License

GNU General Public License v3.0 or later. See [`LICENSE`](LICENSE).

## Links

- LinSpectacles organisation: <https://github.com/linspectacles/>
- LinSpectacles Hub: <https://github.com/linspectacles/linspectacles-hub>
- LinSpectacles Hub Modules: <https://github.com/linspectacles/linspectacles-modules>
- Repository: <https://github.com/linspectacles/linspectacles-metapackages>
