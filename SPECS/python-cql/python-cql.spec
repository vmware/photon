Name:           python3-cql
Version:        1.4.0
Release:        2%{?dist}
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
BuildRequires:  python3-macros
Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
A Python driver for CQL that adheres to py-dbapi v2
(PEP249, Python Database API Specification v2.0: http://www.python.org/dev/peps/pep-0249/).

%prep
%autosetup -n cql-%{version}

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
*   Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.4.0-2
-   Bump up to compile with python 3.10
*   Fri Jun 11 2021 Ankit Jain <ankitja@vmware.com> 1.4.0-1
-   Initial packaging for Photon
