Name:           linspectacles-applets
Version:        0.0.1
Release:        1%{?dist}
Summary:        Official LinSpectacles applet collection metapackage
License:        GPL-3.0-or-later
URL:            https://github.com/linspectacles/linspectacles-metapackages
Vendor:         LinSpectacles
Packager:       brunonlinespace
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Recommends:     linspectacles-autostart-inspector
Recommends:     linspectacles-block-devices
Recommends:     linspectacles-boot-loaders
Recommends:     linspectacles-boot-timing
Recommends:     linspectacles-cgroups-inspector
Recommends:     linspectacles-coredumps-inspector
Recommends:     linspectacles-cpu-vulnerabilities
Recommends:     linspectacles-crypto-registry
Recommends:     linspectacles-dbus-inspector
Recommends:     linspectacles-desktop-integration
Recommends:     linspectacles-display-server
Recommends:     linspectacles-environment-variables
Recommends:     linspectacles-file-handles
Recommends:     linspectacles-filesystem-details
Recommends:     linspectacles-firmware-inspector
Recommends:     linspectacles-gpu-inspector
Recommends:     linspectacles-hardware-topology
Recommends:     linspectacles-initramfs-inspector
Recommends:     linspectacles-input-devices
Recommends:     linspectacles-installed-software
Recommends:     linspectacles-interrupts-inspector
Recommends:     linspectacles-ipc-inspector
Recommends:     linspectacles-journal-inspector
Recommends:     linspectacles-kernel-modules
Recommends:     linspectacles-kernel-pressure
Recommends:     linspectacles-kernel-ring-buffer
Recommends:     linspectacles-kernel-tunables
Recommends:     linspectacles-linux-resmon
Recommends:     linspectacles-login-inspector
Recommends:     linspectacles-mounted-filesystems
Recommends:     linspectacles-namespace-inspector
Recommends:     linspectacles-path-inspector
Recommends:     linspectacles-power-thermal-inspector
Recommends:     linspectacles-problem-finder
Recommends:     linspectacles-python-packages
Recommends:     linspectacles-resolver-inspector
Recommends:     linspectacles-scheduler-inspector
Recommends:     linspectacles-selinux-inspector
Recommends:     linspectacles-systemd-inspector
Recommends:     linspectacles-timekeeping-inspector
Recommends:     linspectacles-tpm-inspector
Recommends:     linspectacles-tty-inspector
Recommends:     linspectacles-virtualisation-inspector
Recommends:     linspectacles-xdg-portals

%description
linspectacles-applets is the convenience metapackage for installing all 44
official LinSpectacles applet RPMs. The applets remain separately packaged,
versioned, upgradeable and removable.

The applet RPMs are recommended weak dependencies rather than mandatory
requirements. Standard DNF installations therefore install the complete
collection by default, while an individual applet may be removed without
requiring removal of this metapackage or the other applets.

This package contains no applet implementation, Hub, Hub Module, helper or
runtime payload. It has no dependency on linspectacles, linspectacles-hub or
linspectacles-modules.

%prep
%autosetup

%build
# Dependency-only metapackage; no build step is required.

%install
# No applet payload is installed by this metapackage.

%files
%license LICENSE
%doc README.md

%changelog
* Tue Nov 17 2026 brunonlinespace - 0.0.1-1
- Initial LinSpectacles applet collection metapackage.
- Recommend all 44 official applet RPMs without exact version pins.
- Keep every applet independently removable while installing the complete set by default under standard DNF weak-dependency behavior.
- Depend on neither linspectacles-hub nor linspectacles-modules.
- Include no applet implementation or runtime payload.
