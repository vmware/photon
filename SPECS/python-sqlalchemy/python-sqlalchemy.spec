%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        The Python SQL Toolkit and Object Relational Mapper
Name:           python-sqlalchemy
Version:        1.3.7
Release:        2%{?dist}
Url:            http://www.sqlalchemy.org
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/29/18/a78469bc449d9f92f6269cc62d0d6fbe6bf394d1031b447ad5e54463c3a0/SQLAlchemy-%{version}.tar.gz
%define sha1    SQLAlchemy=45b36906f108c730577dc81ba5fd16cce37a74be
BuildRequires:  python2-devel
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif
Requires:       python2
Requires:       python2-libs

%description
SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. SQLAlchemy provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.


%prep
%setup -q -n SQLAlchemy-%{version}

%build
python2 setup.py build

%check
easy_install apipkg
easy_install py
easy_install mock
easy_install pytest==4.6
python2 setup.py test

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%changelog
*   Wed Jan 08 2020 Prashant S Chauhan <psinghchauha@vmware.com> 1.3.7-2
-   Added python2-devel as a build requirement
*   Fri Aug 23 2019 Tapas Kundu <tkundu@vmware.com> 1.3.7-1
-   Update to version 1.3.7
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.2.11-1
-   Update to version 1.2.11
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.1.7-2
-   Use python2 explicitly
*   Thu Mar 30 2017 Siju Maliakkal <smaliakal@vmware.com> 1.1.7-1
-   Updating package version to latest
*   Fri Nov 18 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0.15-2
-   Remove noarch
*   Tue Sep 6 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.15-1
-   Initial packaging for Photon
