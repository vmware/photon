%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Pure Python sorted container types
Name:           python-sortedcontainers
Version:        2.2.2
Release:        1%{?dist}
License:        ASL 2.0
URL:            http://www.python.org/
Group:          System Environment/Programming
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/grantjenks/python-sortedcontainers/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha1    python-sortedcontainers=a4f162561c3c5e49e8dde55a393afa0adf5954b2

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

Provides:       python3.8dist(sortedcontainers) = %{version}

%description
SortedContainers is an Apache2 licensed sorted collections library, written in \
pure-Python, and fast as C-extensions.

%prep
%setup -n sortedcontainers-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --root %{buildroot}

%post
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/sortedcontainers-2.2.2-py3.8.egg-info/*
%{python3_sitelib}/sortedcontainers/*

%changelog
*   Sat Sep 19 2020 Susant Sahani <ssahaniv@vmware.com> 2.2.2-1
-   Initial rpm release.
