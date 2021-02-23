%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-argparse
Version:        1.4.0
Release:        1%{?dist}
Url:            https://pypi.org/project/argparse
Summary:        Python command-line parsing library
License:        Python Software Foundation License
Group:          Development/Languages/Python
Source0:        argparse-%{version}.tar.gz
%define sha1    argparse=50f36429b2989461ee541093e7229257ee950c07
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-setuptools
BuildArch:      noarch
Vendor:         VMware, Inc.
Distribution:   Photon

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
%setup -n argparse-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%doc NEWS.txt README.txt doc/*
%python3_sitelib/*

%changelog
*   Tue Feb 23 2021 Tapas Kundu <tkundu@vmware.com> 1.4.0-1
-   Initial build.  First version
