Summary:        A modern IPv4/IPv6 ipcalc tool.
Name:           ipcalc
Version:        0.4.1
Release:        1%{?dist}
License:        GPLv2
URL:            https://gitlab.com/ipcalc/ipcalc
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://gitlab.com/%{name}/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz
%define sha1 ipcalc=bc9a40c99a779b5834f74ecec820b1aaf48de721

%description
ipcalc is a modern tool to assist in network address calculations for IPv4 and
IPv6. It acts both as a tool to output human readable information about a
network or address, as well as a tool suitable to be used by scripts or other
programs.

%prep
%setup -q

%build
make USE_GEOIP=no USE_MAXMIND=no

%install
install -m 755 -D ipcalc %{buildroot}%{_bindir}/ipcalc

%files
%defattr(-,root,root)
%{_bindir}/ipcalc

%changelog
*   Thu Aug 13 2020 Andrew Kutz <akutz@vmware.com> 0.4.1-1
-   Add ipcalc 0.4.1 package
