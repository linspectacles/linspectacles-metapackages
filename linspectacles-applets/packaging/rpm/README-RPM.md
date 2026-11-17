# RPM packaging — linspectacles-applets

This directory contains the Fedora/RPM packaging source for the dependency-only **`linspectacles-applets`** metapackage.

Current metapackage release: **0.0.1**

It contains **no applet implementation source**. Its purpose is to install all 44 official LinSpectacles applet RPMs together while preserving independent applet versions, upgrades and removal.

The 44 applet RPMs are `Recommends:` weak dependencies. Standard DNF installations pull them in by default. An individual applet can therefore be removed without forcing removal of the metapackage or the rest of the applet collection.

## Recommended applet packages

- `linspectacles-autostart-inspector` — Autostart Inspector
- `linspectacles-block-devices` — Block Devices
- `linspectacles-boot-loaders` — Boot Loaders
- `linspectacles-boot-timing` — Boot Timing
- `linspectacles-cgroups-inspector` — Cgroups Inspector
- `linspectacles-coredumps-inspector` — Coredumps Inspector
- `linspectacles-cpu-vulnerabilities` — CPU Vulnerabilities
- `linspectacles-crypto-registry` — Crypto Registry
- `linspectacles-dbus-inspector` — D-Bus Inspector
- `linspectacles-desktop-integration` — Desktop Integration
- `linspectacles-display-server` — Display Server
- `linspectacles-environment-variables` — Environment Variables
- `linspectacles-file-handles` — File Handles
- `linspectacles-filesystem-details` — Filesystem Details
- `linspectacles-firmware-inspector` — Firmware Inspector
- `linspectacles-gpu-inspector` — GPU Inspector
- `linspectacles-hardware-topology` — Hardware Topology
- `linspectacles-initramfs-inspector` — Initramfs Inspector
- `linspectacles-input-devices` — Input Devices
- `linspectacles-installed-software` — Installed Software
- `linspectacles-interrupts-inspector` — Interrupts Inspector
- `linspectacles-ipc-inspector` — IPC Inspector
- `linspectacles-journal-inspector` — Journal Inspector
- `linspectacles-kernel-modules` — Kernel Modules
- `linspectacles-kernel-pressure` — Kernel Pressure
- `linspectacles-kernel-ring-buffer` — Kernel Ring Buffer
- `linspectacles-kernel-tunables` — Kernel Tunables
- `linspectacles-linux-resmon` — Resource Monitor
- `linspectacles-login-inspector` — Login Inspector
- `linspectacles-mounted-filesystems` — Mounted Filesystems
- `linspectacles-namespace-inspector` — Namespace Inspector
- `linspectacles-path-inspector` — Path Inspector
- `linspectacles-power-thermal-inspector` — Power and Thermal Inspector
- `linspectacles-problem-finder` — Problem Finder
- `linspectacles-python-packages` — Python Packages
- `linspectacles-resolver-inspector` — Resolver Inspector
- `linspectacles-scheduler-inspector` — Scheduler Inspector
- `linspectacles-selinux-inspector` — SELinux Inspector
- `linspectacles-systemd-inspector` — Systemd Inspector
- `linspectacles-timekeeping-inspector` — Timekeeping Inspector
- `linspectacles-tpm-inspector` — TPM Inspector
- `linspectacles-tty-inspector` — TTY Inspector
- `linspectacles-virtualisation-inspector` — Virtualisation Inspector
- `linspectacles-xdg-portals` — XDG Portals

There are deliberately no exact version pins.

## Isolation from Hub and Modules

`linspectacles-applets` has no dependency on `linspectacles`, `linspectacles-hub`, `linspectacles-modules`, or individual Hub Module RPMs.

Under DNF's default `clean_requirements_on_remove=True`, removing `linspectacles-applets` makes packages that were installed solely as dependencies of it eligible for cleanup when they are no longer needed. Explicitly user-installed applets can remain by design.

## Fedora build

Install the RPM build tool if necessary:

```bash
sudo dnf install rpm-build
```

From this directory run:

```bash
./build-rpm-fedora.sh
```

The builder recreates its source tarball from the repository `LICENSE` and `linspectacles-applets/README.md` at build time, uses a private temporary RPM work tree, and never deletes an existing output directory.

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

After publication, first preview the complete installation:

```bash
sudo dnf install linspectacles-applets
```

DNF should normally offer all 44 applet RPMs when weak dependencies are enabled.

To verify independent applet removal, preview one applet removal and confirm `linspectacles-applets` is not listed as a dependent removal.

To verify collection removal, preview:

```bash
sudo dnf remove linspectacles-applets
```

Applets installed solely through this metapackage and no longer needed should be eligible for cleanup under the default DNF removal policy. `linspectacles-hub` and `linspectacles-modules` are not dependencies of this package and should not be pulled into the removal merely because this metapackage is removed.
