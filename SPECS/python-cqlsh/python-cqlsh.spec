%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        A Python-based command-line client for running simple CQL commands on a Cassandra cluster.
Name:           python3-cqlsh
Version:        6.0.0b4
Release:        1%{?dist}
License:        Apache License Version 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/cqlsh
Source0:        https://files.pythonhosted.org/packages/source/c/cqlsh/cqlsh-%{version}.tar.gz
%define         sha1 cqlsh=ce422f113eb8b79dcaa1d1f1230b819980d2bb19

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       python3-libs
Requires:       python3-cassandra-driver
Requires:       python3-cql
Requires:       python3-six
Requires:       cassandra

BuildArch:      noarch

%description
cqlsh is a Python-based command-line tool, and the most direct way to run simple CQL commonds on a Cassandra cluster.
This is a simple re-bundling of the open source tool that comes bundled with Cassandra to allow for cqlsh to be installed and run inside of virtual environments..

%prep
%setup -q -n cqlsh-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py check

%files
%defattr(-,root,root)
%{_bindir}/cqlsh
%{python3_sitelib}/*

%changelog
*   Wed Jun 09 2021 Ankit Jain <ankitja@vmware.com> 6.0.0b4-1
-   Update to 6.0.0b4 to support python3
*   Mon Jul 10 2017 Xiaolin Li <xiaolinl@vmware.com> 5.0.4-1
-   Initial packaging for Photon
