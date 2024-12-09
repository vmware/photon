Summary:        Utility to send ICMP echo probes to network hosts
Name:           fping
Version:        5.1
Release:        2%{?dist}
Group:          Productivity/Networking/Diagnostic
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://www.fping.org/
Source0:        http://fping.org/dist/%{name}-%{version}.tar.gz
%define sha512  fping=1a208da8dcd99093d0512af5d85ba5e7b5743ec97993d24c1fe612bb58d93090ac1ba0952f648aa075f16d390a77c4be65e394ae56dbede2a6914e0e8c68e2bd

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  autoconf
BuildRequires:  automake

%description
fping is a ping like program which uses the Internet Control Message Protocol
(ICMP) echo request to determine if a target host is responding.

%prep
%autosetup

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install
ln -sf fping %{buildroot}%{_sbindir}/fping6
rm -rf %{buildroot}%{_infodir}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%{_sbindir}/fping
%{_sbindir}/fping6
%doc CHANGELOG.md COPYING
%doc %{_mandir}/man8/fping.8*

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.1-2
- Release bump for SRP compliance
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 5.1-1
- Automatic Version Bump
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 5.0-1
- Automatic Version Bump
* Wed Jan 23 2019 Dweep Advani <dadvani@vmware.com> 4.1-1
- Added fping package to Photon 2.0
