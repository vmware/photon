Summary:        Exuberant Ctags - a multi-language source code indexing tool
Name:           ctags
Version:        5.8
Release:        3%{?dist}
License:        GPL
URL:            http://ctags.sourceforge.net
Group:          Development/Tools
Buildroot:      %{_tmppath}/%{name}-%{version}-root
Vendor:         VMware, Inc.
Distribution:   Photon

Source:         http://prdownloads.sourceforge.net/ctags/ctags-%{version}.tar.gz
%define sha512 %{name}=981912cd335978cde22864e977947fc75326572fb29518e559cc4a8ac1edc84b3604165218a666e36353f17da4f89f8e967acdb88696f816748eb946d79eaa15

Patch0:         CVE-2014-7204.patch

%description
Exuberant Ctags generates an index (or tag) file of language objects
found in source files for many popular programming languages. This index
makes it easy for text editors and other tools to locate the indexed
items. Exuberant Ctags improves on traditional ctags because of its
multilanguage support, its ability for the user to define new languages
searched by regular expressions, and its ability to generate emacs-style
TAGS files.

%prep
%autosetup -p1

%build
%configure
make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
%makeinstall

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/ctags
%{_mandir}/man1/ctags*

%changelog
* Thu Aug 21 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.8-3
- Fixes CVE-2014-7204
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.8-2
- GA - Bump release of all rpms
* Tue Jul 14 2015 Luis Zuniga <lzuniga@vmware.com> 5.8-1
- Initial build for Photon
