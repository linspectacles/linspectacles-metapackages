Name:           @NAME@
Version:        @VERSION@
Release:        1%{?dist}
Summary:        @SUMMARY@

License:        GPL-3.0-or-later
URL:            @URL@
Vendor:         LinSpectacles
Packager:       brunonlinespace
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3
Requires:       python3
Requires:       python3-pyqt6
@EXTRA_REQUIRES@

%description
@DESCRIPTION@

%prep
%autosetup

%build
# Pure Python/source applet; no build step is required.

%install
APPLET_DIR="%{buildroot}%{_libexecdir}/linspectacles/applets/@PYTHON_ROOT@"
install -d "$APPLET_DIR"
cp -a . "$APPLET_DIR/"
find "$APPLET_DIR" -type d -name __pycache__ -prune -exec rm -rf {} +
find "$APPLET_DIR" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete

install -d "%{buildroot}%{_bindir}"
cat > "%{buildroot}%{_bindir}/%{name}" <<'APPLET_LAUNCHER'
#!/bin/sh
exec /usr/bin/python3 "%{_libexecdir}/linspectacles/applets/@PYTHON_ROOT@/@STANDALONE@" "$@"
APPLET_LAUNCHER
chmod 0755 "%{buildroot}%{_bindir}/%{name}"

@TUI_INSTALL@
@HELPER_INSTALL@

%check
python3 -m compileall -q .

%files
%dir %{_libexecdir}/linspectacles
%dir %{_libexecdir}/linspectacles/applets
%license %{_libexecdir}/linspectacles/applets/@PYTHON_ROOT@/LICENSE
%doc %{_libexecdir}/linspectacles/applets/@PYTHON_ROOT@/README.md
%{_libexecdir}/linspectacles/applets/@PYTHON_ROOT@
%{_bindir}/%{name}
@TUI_FILES@
@HELPER_FILES@

%changelog
* Mon Nov 16 2026 brunonlinespace <brunonlinespace@users.noreply.github.com> - @VERSION@-1
- Package @DISPLAY_NAME@ from its self-describing LinSpectacles applet source.
