%define debug_package %{nil}

Summary:        AsciiDoc is a human readable text document format
Name:           asciidoc3
Version:        3.2.3
Release:        4%{?dist}
URL:            https://gitlab.com/asciidoc3/asciidoc3
Group:          System Environment/Development
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://asciidoc3.org/%{name}-%{version}.tar.gz
%define sha512 %{name}=926f367b1740a40a03beb9c45a05de855e69d8c2ac9b9a66c19dd21f65f8250b3fad02b283f7f8b2fb7ea131d4836d5aa623647e1931b682a9a9e91f62863f6c

Source1: license.txt
%include %{SOURCE1}
Patch0:         asciidoc3-py311.patch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools

Requires:       python3-setuptools
Requires:       python3
Requires:       python3-pip

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
%autosetup -p1 -n %{name}-v%{version}

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
* Wed Dec 11 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 3.2.3-4
- Release bump for SRP compliance
* Tue Jan 09 2024 Prashant S Chauhan <psinghchauha@vmware.com> 3.2.3-3
- Add python3-pip as runtime Requires
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.2.3-2
- Update release to compile with python 3.11
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.2.3-1
- Update to 3.2.3
* Thu Sep 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.2.0-2
- Provde asciidoc from asciidoc3
* Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 3.2.0-1
- Initial build. First version
