# LinSpectacles

**Linux Inspection Suite** — *Expose. Explore. Explain.*

**Convenience RPM metapackage for installing [LinSpectacles Hub](https://github.com/linspectacles/linspectacles-hub) together with the official [LinSpectacles Hub Modules](https://github.com/linspectacles/linspectacles-modules).**

Current metapackage release: **0.0.2**

Source repository: <https://github.com/linspectacles/linspectacles-metapackages>

## What this package is

`linspectacles` is the small dependency-only metapackage for the core LinSpectacles workbench.

It installs:

- `linspectacles-hub` — the LinSpectacles host/workbench.
- `linspectacles-modules` — the metapackage for the official optional Hub Modules.

The package contains **no application runtime, applet implementation, Hub Module implementation, desktop entry, helper binary, or other runtime payload of its own**. Those files remain owned by their individual RPM packages.

There are deliberately no exact dependency-version pins. The Hub and Hub Modules can continue to receive normal independent RPM upgrades without requiring a new `linspectacles` metapackage release unless the package composition itself changes.

## Package relationship

```text
linspectacles
├── linspectacles-hub
└── linspectacles-modules
    ├── linspectacles-module-applet-organizer
    ├── linspectacles-module-boot-environment
    ├── linspectacles-module-encyclopedia
    ├── linspectacles-module-privileged-helpers
    ├── linspectacles-module-system-identity
    └── linspectacles-module-system-pulse
```

Installing this metapackage therefore installs the Hub plus the complete official Hub Module set available through `linspectacles-modules`.

The individual packages remain independently versioned and separately owned. While `linspectacles` is installed, both `linspectacles-hub` and `linspectacles-modules` are required dependencies; removing one of them may also require removing this metapackage.

## Installation

After enabling an RPM repository that provides the LinSpectacles packages:

```bash
sudo dnf install linspectacles
```

This is the convenience installation for the **core LinSpectacles workbench**.

To install only the Hub instead:

```bash
sudo dnf install linspectacles-hub
```

To install only the official Hub Module set:

```bash
sudo dnf install linspectacles-modules
```

This repository does not configure a COPR or other package repository by itself.

## Place in the metapackage family

`linspectacles` is one of the metapackages housed by the `linspectacles-metapackages` repository:

```text
linspectacles-full                         [WIP]
├── linspectacles                          [implemented here]
│   ├── linspectacles-hub
│   └── linspectacles-modules
└── linspectacles-applets                  [WIP]
```

`linspectacles` deliberately does **not** depend on `linspectacles-applets`. That keeps the core Hub/workbench installation separate from the future all-applets bundle and allows `linspectacles-full` to compose both cleanly.

## Package source layout

```text
linspectacles/
├── README.md
└── packaging/
    └── rpm/
        ├── README-RPM.md
        ├── build-rpm-fedora.sh
        └── linspectacles.spec
```

The repository-wide `LICENSE`, validation tooling and GitHub workflow are held at the `linspectacles-metapackages` repository root.

## Fedora RPM source and build

The authoritative spec is:

```text
linspectacles/packaging/rpm/linspectacles.spec
```

From the repository root, prepare the RPM source tarball and spec without requiring `rpmbuild`:

```bash
./linspectacles/packaging/rpm/build-rpm-fedora.sh --prepare-only
```

To build both the binary RPM and SRPM on Fedora:

```bash
sudo dnf install rpm-build
./linspectacles/packaging/rpm/build-rpm-fedora.sh
```

Generated artifacts are written to:

```text
linspectacles/packaging/rpm/dist-rpm/
```

That directory is build output and is intentionally excluded from version control.

See [`packaging/rpm/README-RPM.md`](packaging/rpm/README-RPM.md) for the full build contract.

## Scope

This package expresses **installation composition only**.

It does not:

- merge the Hub and Modules into one runtime package.
- take ownership of files from dependency packages.
- force all applets to be installed.
- replace independent Hub or Module versioning.
- configure a package repository.
- provide an AppStream application or desktop entry of its own.

The normal `/usr/bin/linspectacles` command continues to be provided by `linspectacles-hub`; this dependency-only metapackage does not install a competing launcher.

## License

GNU General Public License v3.0 or later. See [`../LICENSE`](../LICENSE).

## Links

- LinSpectacles organisation: <https://github.com/linspectacles/>
- LinSpectacles Hub: <https://github.com/linspectacles/linspectacles-hub>
- LinSpectacles Hub Modules: <https://github.com/linspectacles/linspectacles-modules>
- Metapackages repository: <https://github.com/linspectacles/linspectacles-metapackages>
