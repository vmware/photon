%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        A Python-based command-line client for running simple CQL commands on a Cassandra cluster.
Name:           python-cqlsh
Version:        5.0.4
Release:        1%{?dist}
License:        Apache License Version 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.python.org/pypi/cqlsh
Source0:        https://files.pythonhosted.org/packages/source/c/cqlsh/cqlsh-%{version}.tar.gz
%define         sha1 cqlsh=d34344538b17e28a3547c571d2bcb50019d6c94f

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs
Requires:       python-cassandra-driver
Requires:       cassandra
Requires:       python-futures
Requires:       python-six

BuildArch:      noarch

%description
cqlsh is a Python-based command-line tool, and the most direct way to run simple CQL commonds on a Cassandra cluster. This is a simple re-bundling of the open source tool that comes bundled with Cassandra to allow for cqlsh to be installed and run inside of virtual environments..

%prep
%setup -q -n cqlsh-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py check

%files
%defattr(-,root,root)
%{python2_sitelib}/*
%{_bindir}/cqlsh

%changelog
*   Mon Jul 10 2017 Xiaolin Li <xiaolinl@vmware.com> 5.0.4-1
-   Initial packaging for Photon
