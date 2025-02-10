%define debug_package %{nil}

Summary:        AsciiDoc is a human readable text document format
Name:           asciidoc3
Version:        3.2.0
Release:        4%{?dist}
License:        GPLv2+
URL:            https://gitlab.com/asciidoc3/asciidoc3
Group:          System Environment/Development
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://asciidoc3.org/%{name}-%{version}.tar.gz
%define sha512 %{name}=31ea277aeb037b7b217e17a2ba54c86b4c7cf923669538b6732120fccd6582097815e5d5ea832ea39c3514068887d4dc5ecafc0d65359794d729cf4711c8e693
Patch0:         build-with-python3.10.patch
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-setuptools
Requires:       python3
Requires:       python3-pip
BuildArch:      noarch

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
mkdir -p %{buildroot}%{_sysconfdir}
mv %{buildroot}/asciidoc3 %{buildroot}%{python3_sitelib}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/*

%changelog
* Thu Feb 06 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.2.0-4
- Bump up release as part of python3-pip upgrade
* Tue Jan 09 2024 Prashant S Chauhan <psinghchauha@vmware.com> 3.2.0-3
- Add python3-pip as runtime Requires
* Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.2.0-2
- Update release to compile with python 3.10
* Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 3.2.0-1
- Initial build.  First version
