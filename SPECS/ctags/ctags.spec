%global build_if %{photon_subrelease} >= 91

%define upstreamversion 20251102.0

Summary:        A C programming language indexing and/or cross-reference tool
Name:           ctags
Version:        6.2
Release:        4%{?dist}
URL:            https://ctags.io/
Source0:        https://github.com/universal-ctags/ctags/archive/%{name}-p%{version}.%{upstreamversion}.tar.gz

Source1: license.txt
%include %{SOURCE1}
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
%if 0%{?with_check} == 0
rm -r Units/parser-typescript.r/ts-class-member-init.d/
%endif

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
* Wed Jun 03 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 6.2-4
- Release version bump as part of libxml2/libxslt
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.2-3
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.2-2
- Bump version as a part of python3.14 upgrade
* Thu Nov 06 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.2-1
- Upgrade to 6.2 version
* Fri Jul 18 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 6.0-4
- Bump up to build with latest jansson
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.0-3
- Release bump for SRP compliance
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 6.0-2
- Bump version as a part of libxml2 upgrade
* Fri Feb 17 2023 Anmol Jain <anmolja@vmware.com> 6.0-1
- Automatic Version Bump
* Mon Sep 19 2022 Anmol Jain <anmolja@vmware.com> 5.9-1
- Migrate to Universal ctags
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.8-2
- GA - Bump release of all rpms
* Tue Jul 14 2015 Luis Zuniga <lzuniga@vmware.com> 5.8-1
- Initial build for Photon
