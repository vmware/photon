Summary:        Exuberant Ctags - a multi-language source code indexing tool
Name:           ctags
Version:        5.8
Release:        2%{?dist}
License:        GPL
URL:            http://ctags.sourceforge.net
Source:         http://prdownloads.sourceforge.net/ctags/ctags-%{version}.tar.gz
%define sha1 ctags=482da1ecd182ab39bbdc09f2f02c9fba8cd20030
Group:          Development/Tools
Buildroot:      %{_tmppath}/%{name}-%{version}-root
Vendor:         VMware, Inc.
Distribution:   Photon

%description
Exuberant Ctags generates an index (or tag) file of language objects
found in source files for many popular programming languages. This index
makes it easy for text editors and other tools to locate the indexed
items. Exuberant Ctags improves on traditional ctags because of its
multilanguage support, its ability for the user to define new languages
searched by regular expressions, and its ability to generate emacs-style
TAGS files.

%prep
%setup -q

%build
%configure
make

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
%makeinstall

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/ctags
%{_mandir}/man1/ctags*

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>         5.8-2
-	GA - Bump release of all rpms
* Tue Jul 14 2015 Luis Zuniga <lzuniga@vmware.com> 5.8-1
- Initial build for Photon
