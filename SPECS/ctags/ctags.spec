%define upstreamversion 20230212.0

Summary:        A C programming language indexing and/or cross-reference tool
Name:           ctags
Version:        6.0
Release:        2%{?dist}
License:        GPL
URL:            https://ctags.io/
Source:         https://github.com/universal-ctags/ctags/archive/%{name}-%{version}.%{upstreamversion}.tar.gz
%define sha512 ctags=976aaf8c87ab35019ea621ed67781f652ac43250a042708a80e063faa827fa9ecf69ad751a28a09ecb56a9f767a3c79d3a91fbb6cf9625daf3426f8c7f4eb871
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  jansson-devel
BuildRequires:  libseccomp-devel
BuildRequires:  libxml2-devel
BuildRequires:  libyaml-devel
BuildRequires:  make
BuildRequires:  python3-docutils

%description
Universal Ctags (abbreviated as u-ctags) is a maintained implementation of ctags.
ctags generates an index (or tag) file of language objects found in source files
for programming languages. This index makes it easy for text editors and other
tools to locate the indexed items.

%prep
%autosetup -p1 -n %{name}-p%{version}.%{upstreamversion}

%build
./autogen.sh
%configure

%make_build

%install
%make_install

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_bindir}/optscript
%{_bindir}/readtags
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%changelog
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.0-2
- Bump version as a part of libxml2 upgrade
* Fri Feb 17 2023 Anmol Jain <anmolja@vmware.com> 6.0-1
- Automatic Version Bump
* Mon Sep 19 2022 Anmol Jain <anmolja@vmware.com> 5.9-1
- Migrate to Universal ctags
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.8-2
- GA - Bump release of all rpms
* Tue Jul 14 2015 Luis Zuniga <lzuniga@vmware.com> 5.8-1
- Initial build for Photon
