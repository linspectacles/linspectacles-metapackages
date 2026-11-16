# LinSpectacles Metapackages

**Dependency-only RPM metapackages for composing LinSpectacles installation sets.**

Current repository release: **0.0.2**

Repository: <https://github.com/linspectacles/linspectacles-metapackages>

## What this repository is

`linspectacles-metapackages` is the source repository for the small dependency-only RPM packages that compose larger LinSpectacles installation sets.

It does **not** duplicate the Hub, Hub Modules, or inspector applet sources. Those remain in their own repositories and continue to own their own runtime files and RPM packaging.

The metapackages here only express installation relationships between those independently packaged components.

## Metapackage family

| Metapackage | Composition | Status |
| --- | --- | --- |
| **`linspectacles`** | `linspectacles-hub` + `linspectacles-modules` | **Available — 0.0.2** |
| `linspectacles-applets` | All official LinSpectacles applet RPMs | **Work in progress** |
| `linspectacles-full` | `linspectacles` + `linspectacles-applets` | **Work in progress** |

The intended package relationship is:

```text
linspectacles-full                         [WIP]
├── linspectacles
│   ├── linspectacles-hub
│   └── linspectacles-modules
└── linspectacles-applets                  [WIP]
    └── all official LinSpectacles applet RPMs
```

Only **`linspectacles`** is implemented in this repository release. The two future package directories are deliberately documentation-only placeholders and contain no RPM spec or dependency contract yet.

## Repository layout

```text
linspectacles-metapackages/
├── .github/
│   ├── REPOSITORY-ABOUT.md
│   └── workflows/
│       └── validate.yml
├── linspectacles/
│   ├── README.md
│   └── packaging/
│       └── rpm/
│           ├── README-RPM.md
│           ├── build-rpm-fedora.sh
│           └── linspectacles.spec
├── linspectacles-applets/
│   └── README.md
├── linspectacles-full/
│   └── README.md
├── tools/
│   └── validate_repository.py
├── .gitignore
├── LICENSE
└── README.md
```

This layout is intentional: each metapackage occupies a sibling directory, while repository-wide documentation, validation, workflows and licensing remain at the repository root.

## Implemented metapackage: linspectacles

The currently implemented metapackage requires exactly:

```text
linspectacles-hub
linspectacles-modules
```

It has no runtime payload of its own and deliberately has no exact dependency-version pins.

See [`linspectacles/README.md`](linspectacles/README.md) for the package contract and build instructions.

## Existing dependency repositories

The dependencies remain separately developed and packaged:

- LinSpectacles Hub: <https://github.com/linspectacles/linspectacles-hub>
- LinSpectacles Hub Modules: <https://github.com/linspectacles/linspectacles-modules>

Nothing from either repository is vendored into this metapackage repository.

## Validation

Run the repository checks with:

```bash
python3 tools/validate_repository.py
```

The validator checks the repository layout, the implemented `linspectacles` package identity and exact dependency contract, the WIP boundaries for the future sibling metapackages, shell syntax, and RPM source generation.

## License

GNU General Public License v3.0 or later. See [`LICENSE`](LICENSE).

## Links

- LinSpectacles organisation: <https://github.com/linspectacles/>
- LinSpectacles Hub: <https://github.com/linspectacles/linspectacles-hub>
- LinSpectacles Hub Modules: <https://github.com/linspectacles/linspectacles-modules>
- Repository: <https://github.com/linspectacles/linspectacles-metapackages>
