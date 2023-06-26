Summary:       ISO-9660 and Rock Ridge image manipulation tool
Name:          xorriso
Version:       1.5.2
Release:       2%{?dist}
License:       GPL-2.0 GPL-3.0 LGPL-2.1
URL:           https://mirrors.kernel.org/gnu/xorriso/%{name}-%{version}.tar.gz
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: https://mirrors.kernel.org/gnu/xorriso/%{name}-%{version}.tar.gz
%define sha512 %{name}=7247c00cda11a5341ab100f1091200e396b76cb5c852a3958fe3b9b735aa6a9142a0f22d2892275887bf52de175776e731fd853fff8c6ce20a096435fa05daf9

BuildRequires: acl
BuildRequires: attr-devel
BuildRequires: bzip2
BuildRequires: pkg-config
BuildRequires: zlib

%description
Xorriso is a program which copies file objects from POSIX compliant
filesystems into Rock Ridge enhanced ISO-9660 filesystems and allows
session-wise manipulation of such filesystems.

%package doc
Summary: Documentation for xorriso package
Group:   Documentation

%description doc
Documentation for xorriso package

%prep
%autosetup -p1

%build
export LANG=C

%configure \
    --disable-static

%make_build

%if 0%{?with_check}
%check
export LANG=C
%make_build check
%endif

%install
%make_install %{?_smp_mflags}

%files
%defattr(-,root,root,-)
%exclude %{_bindir}/xorriso-tcltk
%{_bindir}/xorrisofs
%{_bindir}/xorrecord
%{_bindir}/osirrox
%{_bindir}/xorriso

%files doc
%defattr(-,root,root,-)
%doc %{_mandir}/man1/*
%doc %{_infodir}/*
%exclude %{_infodir}/dir

%changelog
* Fri Jan 22 2021 Dweep Advani <dadvani@vmware.com> 1.5.2-2
- Removing /usr/share/info/dir from packaging to avoid conflicts
* Thu Jun 25 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.2-1
- Automatic Version Bump
* Tue Jun 12 2018 Keerthana K <keerthanak@vmware.com> 1.4.8-1
- Initial build. First Version
