Summary:        m4 macros used by all of the Xorg packages.
Name:           util-macros
Version:        1.19.3
Release:        2%{?dist}
URL:            http://www.x.org
Group:          Development/System
BuildArch:      noarch
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/util/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}

%description
The util-macros package contains the m4 macros used by all of the Xorg packages.

%prep
%autosetup -p1

%build
%configure

%install
%make_install %{?_smp_mflags}

%ldconfig_scriptlets

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_datadir}/aclocal/xorg-macros.m4
%{_datadir}/pkgconfig/xorg-macros.pc
%{_datadir}/util-macros

%changelog
* Wed Dec 11 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 1.19.3-2
- Release bump for SRP compliance
* Wed Dec 14 2022 Gerrit Photon <photon-checkins@vmware.com> 1.19.3-1
- Automatic Version Bump
* Fri May 15 2015 Alexey Makhalov <amakhalov@vmware.com> 1.19.0-1
- initial version
