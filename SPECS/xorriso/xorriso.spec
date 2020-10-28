Summary:       ISO-9660 and Rock Ridge image manipulation tool
Name:          xorriso
Version:       1.4.8
Release:       2%{?dist}
License:       GPL-2.0 GPL-3.0 LGPL-2.1
URL:           https://mirrors.kernel.org/gnu/xorriso/%{name}-%{version}.tar.gz
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       https://mirrors.kernel.org/gnu/xorriso/%{name}-%{version}.tar.gz
%define sha1   xorriso=44a8412ee19807695181fee06b9569d3fe442e52
BuildRequires: acl
BuildRequires: attr
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
%setup -q -n %{name}-%{version}

%build
export LANG=C
%configure --disable-static
make  %{?_smp_mflags}

%check
export LANG=C
make VERBOSE=1 V=1 %{?_smp_mflags} check

%install
rm -rf %{buildroot}
%make_install

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
* Tue Oct 27 2020 Dweep Advani <dadvani@vmware.com> 1.4.8-2
- Removing /usr/share/info/dir from packaging
* Tue Jun 12 2018 Keerthana K <keerthanak@vmware.com> 1.4.8-1
- Initial build. First Version

