%define upstreamversion 20221009.0

Summary:        A C programming language indexing and/or cross-reference tool
Name:           ctags
Version:        5.9
Release:        1%{?dist}
License:        GPL
URL:            https://ctags.io/
Source:         https://github.com/universal-ctags/ctags/archive/%{name}-%{version}.%{upstreamversion}.tar.gz
%define sha512 ctags=7a317f3e7e7dc90da6f0f86235b8775dd7bf8e90bff4780e8a2d4d51b4f2c820fd7955b36ee6a2bfb9b8bffdd7e78a42cd9ed26af11f6bf606035d8fd2b96764
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
* Mon Sep 19 2022 Anmol Jain <anmolja@vmware.com> 5.9-1
- Migrate to Universal ctags
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.8-2
- GA - Bump release of all rpms
* Tue Jul 14 2015 Luis Zuniga <lzuniga@vmware.com> 5.8-1
- Initial build for Photon
