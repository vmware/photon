Summary:        A modern IPv4/IPv6 ipcalc tool.
Name:           ipcalc
Version:        1.0.1
Release:        1%{?dist}
License:        GPLv2
URL:            https://gitlab.com/ipcalc/ipcalc
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://gitlab.com/%{name}/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz
%define sha512  ipcalc=967396f0bd7f455d90049bf827f7109fc819a6d4a6635fd06a38490e8feb2ce754ebc26064953e7fe42eaee2b0501f0493615dcb6a11d259face3c5d8ae84cc5

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
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.1-1
-   Automatic Version Bump
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.0.0-1
-   Automatic Version Bump
*   Thu Aug 13 2020 Andrew Kutz <akutz@vmware.com> 0.4.1-1
-   Add ipcalc 0.4.1 package
