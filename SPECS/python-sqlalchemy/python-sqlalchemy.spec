Summary:        The Python SQL Toolkit and Object Relational Mapper
Name:           python-sqlalchemy
Version:        1.1.7
Release:        1%{?dist}
Url:            http://www.sqlalchemy.org
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/29/18/a78469bc449d9f92f6269cc62d0d6fbe6bf394d1031b447ad5e54463c3a0/SQLAlchemy-%{version}.tar.gz
%define sha1 SQLAlchemy=9f7ba90b47f79ca556097f5eeea3b82c4a0ec6f2
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs

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
*   Fri Nov 18 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0.15-2
-   Remove noarch
*   Tue Sep 6 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.15-1
-   Initial packaging for Photon
