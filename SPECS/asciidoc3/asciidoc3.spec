%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
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
Source0:        https://asciidoc3.org/asciidoc3-3.2.0.tar.gz
%define sha1 asciidoc3=496a8c515dbb962a9fd3ced810d514cae7677071

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-lxml
BuildRequires:  docbook-xsl
BuildRequires:  docbook-xml
BuildRequires:  automake
BuildRequires:  autoconf

Requires:       python3-setuptools
Requires:       python3
Requires:       python3-xml
Requires:       python3-lxml
Requires:       docbook-xsl
Requires:       docbook-xml

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
%setup

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}
mv %{buildroot}/asciidoc3 %{buildroot}%{python3_sitelib}


%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/*

%changelog
*   Fri Sep 18 2020 Susant Sahani <ssahani@vmware.com> 3.2.0-2
-   Add requires python3-xml
*   Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 3.2.0-1
-   Initial build.  First version
