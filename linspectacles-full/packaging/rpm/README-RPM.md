# RPM packaging — linspectacles-full

This directory contains the Fedora/RPM packaging source for the dependency-only **`linspectacles-full`** metapackage.

Current metapackage release: **0.0.1**

It contains no LinSpectacles runtime payload. Its only purpose is to compose the two sibling metapackages:

```text
Requires: linspectacles
Requires: linspectacles-applets
```

There are deliberately no exact version pins and no duplicated Hub, Modules, or applet dependency lists.

## Fedora build

Install the RPM build tool if necessary:

```bash
sudo dnf install rpm-build
```

From this directory run:

```bash
./build-rpm-fedora.sh
```

The builder recreates its source tarball from the repository `LICENSE` and `linspectacles-full/README.md` at build time, uses a private temporary RPM work tree, and never deletes an existing output directory.

Generated binary RPMs, SRPMs, the source tarball and generated spec are written to:

```text
dist-rpm/
```

To prepare the spec and source tarball without `rpmbuild`:

```bash
./build-rpm-fedora.sh --prepare-only
```

If `RPM_TOPDIR` is set, it must name an existing, whitespace-free parent directory for the temporary work tree. Set `KEEP_BUILD=1` to retain that tree for debugging.

## Install/removal checks

After publication, preview installation with:

```bash
sudo dnf install linspectacles-full
```

DNF should require the `linspectacles` and `linspectacles-applets` metapackages. Their own dependency policies then determine the Hub, Modules, and applet set installed beneath them.

To confirm applet independence, preview removal of one applet and verify that `linspectacles-full`, `linspectacles-applets`, and the rest of the applet collection are not required to be removed solely because that applet is removed.
