Name:           python3-argparse
Version:        1.4.0
Release:        2%{?dist}
Url:            https://pypi.org/project/argparse
Summary:        Python command-line parsing library
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: argparse-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.4.0-2
- Release bump for SRP compliance
* Tue Feb 23 2021 Tapas Kundu <tkundu@vmware.com> 1.4.0-1
- Initial build.  First version
