Name:           python3-argparse
Version:        1.4.0
Release:        1%{?dist}
Url:            https://pypi.org/project/argparse
Summary:        Python command-line parsing library
License:        Python Software Foundation License
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: argparse-%{version}.tar.gz
%define sha512 argparse=9941f9d26c43169f947c9efadda6239349e1f9df80ff5fcdba3070bc7b43c43ab6bb4b7f0c7eee8e5d06231a17a7e9ee9eb73c7a9bb68ebe5d13f879686d61b2

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       python3-setuptools

BuildArch:      noarch

%description
The argparse module provides an easy, declarative interface for
creating command line tools, which knows how to:

* parse the arguments and flags from sys.argv
* convert arg strings into objects for your program
* format and print informative help messages
* and much more...

The argparse module improves on the standard library optparse module
in a number of ways including:

* handling positional arguments
* supporting sub-commands
* allowing alternative option prefixes like + and /
* handling zero-or-more and one-or-more style arguments
* producing more informative usage messages
* providing a much simpler interface for custom types and actions

%prep
%autosetup -p1 -n argparse-%{version}

%build
%py3_build

%install
%py3_install

%files
%defattr(-,root,root,-)
%python3_sitelib/*

%changelog
* Tue Feb 23 2021 Tapas Kundu <tkundu@vmware.com> 1.4.0-1
- Initial build.  First version
