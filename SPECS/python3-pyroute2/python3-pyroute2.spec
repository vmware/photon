%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Pure Python netlink library
Name:           python3-pyroute2
Version:        0.5.17
Release:        1%{?dist}
License:        Apache Software License, GNU General Public License v2 or later (GPLv2+) (dual license GPLv2+ and Apache v2)
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/svinota/pyroute2
Source0:        https://pypi.io/packages/source/p/pyroute2/pyroute2-%{version}.tar.gz
%define sha1    pyroute2=26491aa271fd4649290164b6aaef80c7b078a1a0

BuildRequires:  python3
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-setuptools
Requires:       python3-xml
BuildArch:      noarch

%description
The pyroute2 library consists of a common netlink messages coder / decoder
and a number of protocol-specific modules. It may be used to work with
existing protocols such as RTNL as well as to create your own netlink protocols.

%prep
%setup -q -n pyroute2-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --skip-build --root=%{buildroot}

%files
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/ss2
%{_bindir}/pyroute2-cli
%doc README* LICENSE.GPL.v2 LICENSE.Apache.v2

%changelog
*  Wed Apr 07 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.5.17-1
-  Initial Packaging for pyroute2
