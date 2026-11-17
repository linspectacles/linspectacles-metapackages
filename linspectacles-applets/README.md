# LinSpectacles Applets — RPM metapackage

`linspectacles-applets` is the optional dependency-only RPM metapackage for installing the complete official LinSpectacles applet collection.

Current metapackage release: **0.0.1**

Repository: <https://github.com/linspectacles/linspectacles-metapackages>

## Dependency model

The metapackage contains no applet implementation or runtime executable. It **recommends** all 44 official applet RPMs rather than requiring them.

With Fedora/DNF's normal weak-dependency behavior, installing:

```bash
sudo dnf install linspectacles-applets
```

installs the full applet collection by default.

Because the applets are `Recommends:` weak dependencies, removing one applet does **not** require removing `linspectacles-applets` or the remaining applets.

When `linspectacles-applets` itself is removed with DNF's normal `clean_requirements_on_remove` behavior enabled, applets that DNF installed solely because of this metapackage and that are no longer needed become eligible for automatic cleanup. An applet that was explicitly installed by the user, or is required for another reason, may remain installed.

This metapackage deliberately has **no dependency** on:

- `linspectacles`
- `linspectacles-hub`
- `linspectacles-modules`
- any `linspectacles-module-*` package

Removing the applet collection therefore does not make the Hub or Hub Modules dependencies of this metapackage's removal transaction.

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

There are deliberately no exact version pins. Individual applet RPMs keep their own release cadence. The metapackage needs a new release only when the official collection composition changes or its dependency policy changes.

## RPM build

The RPM source and builder are under [`packaging/rpm/`](packaging/rpm/).

Build the binary RPM and SRPM on Fedora with:

```bash
cd linspectacles-applets/packaging/rpm
./build-rpm-fedora.sh
```

Or prepare only the spec and source tarball:

```bash
./build-rpm-fedora.sh --prepare-only
```

The generated artifacts are written to `packaging/rpm/dist-rpm/`.

## Applet RPM factory

The existing Applet RPM Factory remains under [`factory/`](factory/) and is separate from this dependency-only metapackage. The factory builds and publishes individual applet RPM sources; the metapackage only composes the already-packaged applet set.

## License

GNU General Public License v3.0 or later. See [`../LICENSE`](../LICENSE).
