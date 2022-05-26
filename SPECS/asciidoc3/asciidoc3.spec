%define debug_package %{nil}

Summary:        AsciiDoc is a human readable text document format
Name:           asciidoc3
Version:        3.2.0
Release:        2%{?dist}
License:        GPLv2+
URL:            https://gitlab.com/asciidoc3/asciidoc3
Group:          System Environment/Development
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://asciidoc3.org/%{name}-%{version}.tar.gz
%define sha512 %{name}=31ea277aeb037b7b217e17a2ba54c86b4c7cf923669538b6732120fccd6582097815e5d5ea832ea39c3514068887d4dc5ecafc0d65359794d729cf4711c8e693

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3-setuptools
Requires:       python3

BuildArch:      noarch

Provides:       asciidoc

%description
AsciiDoc3 is a text document format for writing notes, documentation,
articles, books, ebooks, slideshows, web pages, man pages and blogs.
AsciiDoc3 files can be translated to many formats including HTML, PDF,
EPUB, man page, and DocBook markup. AsciiDoc3 is highly configurable:
both the AsciiDoc3 source file syntax and the backend output markups
(which can be almost any type of SGML/XML markup) can be customized
and extended by the user.

%prep
%autosetup -p1

%build
%{py3_build}

%install
%{py3_install}
mv %{buildroot}/%{name} %{buildroot}%{python3_sitelib}
ln -sfv %{_bindir}/%{name} %{buildroot}%{_bindir}/asciidoc

%clean
rm -rf %{buildroot}/*

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/*

%changelog
* Thu Sep 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.2.0-2
- Provde asciidoc from asciidoc3
* Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 3.2.0-1
- Initial build. First version
