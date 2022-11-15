Name:           python3-cql
Version:        1.4.0
Release:        1%{?dist}
Summary:        Cassandra Query Language driver
License:        Apache Software License
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Languages/Python
Url:            https://pypi.org/project/cql

Source0: cql-%{version}.tar.gz
%define sha512 cql=082ada585b81c3b836a6cce218c276c550608e7260083ca2c60d46316f8f203fd9773ffe820d387a09cf00c7d75b0230e99373766fc0b394ee87049f77cf96b1

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

BuildArch:      noarch

%description
A Python driver for CQL that adheres to py-dbapi v2
(PEP249, Python Database API Specification v2.0: http://www.python.org/dev/peps/pep-0249/).

%prep
%autosetup -p1 -n cql-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
python3 setup.py test
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Fri Jun 11 2021 Ankit Jain <ankitja@vmware.com> 1.4.0-1
- Initial packaging for Photon
