Summary:        A modern IPv4/IPv6 ipcalc tool.
Name:           ipcalc
Version:        1.0.2
Release:        2%{?dist}
URL:            https://gitlab.com/ipcalc/ipcalc
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://gitlab.com/%{name}/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
*   Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.0.2-2
-   Release bump for SRP compliance
*   Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.2-1
-   Automatic Version Bump
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.1-1
-   Automatic Version Bump
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.0.0-1
-   Automatic Version Bump
*   Thu Aug 13 2020 Andrew Kutz <akutz@vmware.com> 0.4.1-1
-   Add ipcalc 0.4.1 package
