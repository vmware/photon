Summary:       ISO-9660 and Rock Ridge image manipulation tool
Name:          xorriso
Version:       1.5.2
Release:       1%{?dist}
License:       GPL-2.0 GPL-3.0 LGPL-2.1
URL:           https://mirrors.kernel.org/gnu/xorriso/%{name}-%{version}.tar.gz
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       https://mirrors.kernel.org/gnu/xorriso/%{name}-%{version}.tar.gz
%define sha1   xorriso=98bab86082614a1a0f9601db5c9da14e5ad2d440
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

%changelog
*    Thu Jun 25 2020 Gerrit Photon <photon-checkins@vmware.com> 1.5.2-1
-    Automatic Version Bump
*    Tue Jun 12 2018 Keerthana K <keerthanak@vmware.com> 1.4.8-1
-    Initial build. First Version
