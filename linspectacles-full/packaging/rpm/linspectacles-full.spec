Name:           linspectacles-full
Version:        0.0.1
Release:        1%{?dist}
Summary:        Complete LinSpectacles installation metapackage
License:        GPL-3.0-or-later
URL:            https://github.com/linspectacles/linspectacles-metapackages
Vendor:         LinSpectacles
Packager:       brunonlinespace
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:       linspectacles
Requires:       linspectacles-applets

%description
linspectacles-full is the convenience metapackage for installing the complete
LinSpectacles environment through the existing linspectacles and
linspectacles-applets metapackages.

The lower-level metapackages remain responsible for their own dependency
policies: linspectacles composes the Hub and recommended Hub Modules, while
linspectacles-applets composes the official applet collection. This package
does not duplicate those dependency lists and contains no runtime payload.

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
* Tue Nov 17 2026 brunonlinespace - 0.0.1-1
- Initial complete LinSpectacles installation metapackage.
- Require the linspectacles and linspectacles-applets sibling metapackages.
- Delegate Hub, Modules, and applet dependency policy to those lower-level metapackages.
- Include no runtime payload and use no exact dependency-version pins.
