%define upstreamversion 20251102.0

Summary:        A C programming language indexing and/or cross-reference tool
Name:           ctags
Version:        6.2
Release:        1%{?dist}
License:        GPL
URL:            https://ctags.io/
Source0:        https://github.com/universal-ctags/ctags/archive/%{name}-p%{version}.%{upstreamversion}.tar.gz
%define sha512  %{name}=b3d670e1a9b4535ad17e4fc002e80132dbf02c4cb8de56e60259831cb765b1a0537f51b4c9a8c29c20f1f71de6b714dd4522dd8109048a8fdffed627eaca5a89

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

%changelog
* Wed Nov 05 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 6.2-1
- Change to universal-ctags
- Fixes CVE-2022-4515
* Thu Aug 21 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.8-3
- Fixes CVE-2014-7204
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.8-2
- GA - Bump release of all rpms
* Tue Jul 14 2015 Luis Zuniga <lzuniga@vmware.com> 5.8-1
- Initial build for Photon
