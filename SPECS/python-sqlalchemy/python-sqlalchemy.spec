Summary:        The Python SQL Toolkit and Object Relational Mapper
Name:           python-sqlalchemy
Version:        1.0.15
Release:        1%{?dist}
Url:            http://www.sqlalchemy.org
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/18/7d/f230ac50198cfe3cdc957c3572a18dc92600047ce707b5b923c56ab92c1b/SQLAlchemy-%{version}.tar.gz
%define sha1 SQLAlchemy=b510372c8ee29772b85042dae4f3ba9a1e4d0e2e
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. SQLAlchemy provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.


%prep
%setup -q -n SQLAlchemy-%{version}

%build
python setup.py build

%check
easy_install apipkg
easy_install py
easy_install mock
export PYTHONPATH=$PYTHONPATH:%{_builddir}/SQLAlchemy-%{version}/.eggs/pytest-3.0.3-py2.7.egg
%{__python} setup.py test

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%{python_sitelib}/*

%changelog
*   Tue Sep 6 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.15-1
-   Initial packaging for Photon
