Summary:        m4 macros used by all of the Xorg packages.
Name:           util-macros
Version:        1.19.0
Release:        1%{?dist}
License:        MIT
URL:            http://www.x.org
Group:          Development/System
BuildArch:      noarch
Vendor:         VMware, Inc.
Distribution:   Photon
Source0: http://ftp.x.org/pub/individual/util/%{name}-%{version}.tar.bz2
%define sha512 %{name}=6820fced14e28d505ed47c4e7e9fae17340e93caf94cc983683128b53833e257aed636bcac6204ed87ddc10132473ceb4bd2f6de53ea66ab8f71b8cd23fbfc15
Requires:       pkg-config

%description
The util-macros package contains the m4 macros used by all of the Xorg packages.

%prep
%autosetup -p1

%build
%configure

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} -k check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_datadir}/aclocal/xorg-macros.m4
%{_datadir}/pkgconfig/xorg-macros.pc
%{_datadir}/util-macros

%changelog
* Thu Dec 22 2022 Harinadh D <hdommaraju@vmware.com> 1.19.0-1
- initial release
