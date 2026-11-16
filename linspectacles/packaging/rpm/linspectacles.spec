Name:           linspectacles
Version:        0.0.2
Release:        1%{?dist}
Summary:        LinSpectacles core workbench metapackage
License:        GPL-3.0-or-later
URL:            https://github.com/linspectacles/linspectacles-metapackages
Vendor:         LinSpectacles
Packager:       brunonlinespace
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:       linspectacles-hub
Requires:       linspectacles-modules

%description
linspectacles is the convenience metapackage for installing the LinSpectacles
Hub together with the complete official LinSpectacles Hub Modules set.

This package contains no application, applet, Hub Module, helper or runtime
payload. The Hub and Modules remain separately packaged, versioned and
upgradeable. Removing one of the required packages may also require removing
this metapackage.

%prep
%autosetup

%build
# Dependency-only metapackage; no build step is required.

%install
# No runtime payload is installed by this metapackage.

%files
%license LICENSE
%doc README.md

%changelog
* Mon Nov 16 2026 brunonlinespace - 0.0.2-1
- Move the metapackage source into the shared linspectacles-metapackages repository layout.
- Update the canonical source repository to linspectacles-metapackages.
- Keep the dependency contract unchanged: linspectacles-hub plus linspectacles-modules, without exact version pins.
- Keep linspectacles-applets and linspectacles-full as unimplemented sibling metapackages.

* Mon Nov 16 2026 brunonlinespace - 0.0.1-1
- Initial LinSpectacles core workbench metapackage.
- Require linspectacles-hub and linspectacles-modules without exact version pins.
- Include no application, applet, Module, helper or launcher runtime payload.
- Reserve the sibling package model for future linspectacles-applets and linspectacles-full metapackages.
