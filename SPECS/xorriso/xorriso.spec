Summary:         ISO-9660 and Rock Ridge image manipulation tool
Name:            xorriso
Version:         1.5.4
Release:         4%{?dist}
URL:             https://mirrors.kernel.org/gnu/xorriso/%{name}-%{version}.tar.gz
Group:           Development/Tools
Vendor:          VMware, Inc.
Distribution:    Photon

Source0: https://mirrors.kernel.org/gnu/xorriso/%{name}-%{version}.tar.gz
%define sha512 %{name}=d12c7769e5cca74fc0a15d9cba6bbc652976aab45df1291e524e1b0841d6be1fac15c17f2c34bbc3fbdd320f2c74dcdf663968b766f80a2e95d203d9b9d6c581

Source1: license.txt
%include %{SOURCE1}

BuildRequires: acl
BuildRequires: attr-devel
BuildRequires: bzip2-devel
BuildRequires: pkg-config
BuildRequires: zlib-devel
BuildRequires: readline-devel

Requires: bzip2-libs
Requires: readline
Requires: zlib

%description
Xorriso is a program which copies file objects from POSIX compliant
filesystems into Rock Ridge enhanced ISO-9660 filesystems and allows
session-wise manipulation of such filesystems.

%package         doc
Summary:         Documentation for xorriso package
Group:           Documentation

%description     doc
Documentation for xorriso package

%prep
%autosetup -p1

%build
export LANG=C
%configure \
    --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
export LANG=C
%make_build check
%endif

%files
%defattr(-,root,root,-)
%exclude %{_bindir}/%{name}-tcltk
%{_bindir}/xorrisofs
%{_bindir}/xorrecord
%{_bindir}/osirrox
%{_bindir}/%{name}
%{_bindir}/%{name}-dd-target

%files doc
%defattr(-,root,root,-)
%doc %{_mandir}/man1/*
%doc %{_infodir}/*
%exclude %{_infodir}/dir

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.5.4-4
- Release bump for SRP compliance
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.5.4-3
- Bump version as a part of zlib upgrade
* Thu Dec 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.5.4-2
- Bump version as a part of readline upgrade
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.5.4-1
- Automatic Version Bump
* Fri Jan 22 2021 Dweep Advani <dadvani@vmware.com> 1.5.2-2
- Removing /usr/share/info/dir from packaging to avoid conflicts
* Thu Jun 25 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.2-1
- Automatic Version Bump
* Tue Jun 12 2018 Keerthana K <keerthanak@vmware.com> 1.4.8-1
- Initial build. First Version
