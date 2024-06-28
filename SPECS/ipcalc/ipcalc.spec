Summary:        A modern IPv4/IPv6 ipcalc tool.
Name:           ipcalc
Version:        1.0.2
Release:        1%{?dist}
License:        GPLv2
URL:            https://gitlab.com/ipcalc/ipcalc
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://gitlab.com/%{name}/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz
%define sha512  ipcalc=af0bf4679c09b43853a4254889f733a68ef5e390d1ed390e5f5da5859e818d9a3a95ec7faba42926c5eb1e510aa3c69807f6927047161ca9e7e9f928ec0ffc66

%description
ipcalc is a modern tool to assist in network address calculations for IPv4 and
IPv6. It acts both as a tool to output human readable information about a
network or address, as well as a tool suitable to be used by scripts or other
programs.

%prep
%autosetup

%build
make USE_GEOIP=no USE_MAXMIND=no %{?_smp_mflags}

%install
install -m 755 -D ipcalc %{buildroot}%{_bindir}/ipcalc

%files
%defattr(-,root,root)
%{_bindir}/ipcalc

%changelog
*   Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.2-1
-   Automatic Version Bump
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.1-1
-   Automatic Version Bump
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.0.0-1
-   Automatic Version Bump
*   Thu Aug 13 2020 Andrew Kutz <akutz@vmware.com> 0.4.1-1
-   Add ipcalc 0.4.1 package
