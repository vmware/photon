%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-cql
Version:        1.4.0
Release:        1%{?dist}
Summary:        Cassandra Query Language driver
License:        Apache Software License
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Languages/Python
Url:            https://pypi.python.org/packages/source/s/cql/cql-%{version}.tar.gz
Source0:        cql-%{version}.tar.gz
%define sha1    cql=9bf5d1fa9874885bd2d0419081e5d3a7708167c9

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
A Python driver for CQL that adheres to py-dbapi v2
(PEP249, Python Database API Specification v2.0: http://www.python.org/dev/peps/pep-0249/).

%prep
%setup -n cql-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Jun 11 2021 Ankit Jain <ankitja@vmware.com> 1.4.0-1
-   Initial packaging for Photon
