Summary:        The Python SQL Toolkit and Object Relational Mapper
Name:           python3-sqlalchemy
Version:        1.4.40
Release:        3%{?dist}
Url:            http://www.sqlalchemy.org
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/29/18/a78469bc449d9f92f6269cc62d0d6fbe6bf394d1031b447ad5e54463c3a0/SQLAlchemy-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs

%description
SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. SQLAlchemy provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.

%prep
%autosetup -n SQLAlchemy-%{version}

%build
%py3_build

%check
easy_install apipkg
easy_install py
easy_install mock
export PYTHONPATH=$PYTHONPATH:%{_builddir}/SQLAlchemy-%{version}/.eggs/pytest-3.0.3-py2.7.egg
python3 setup.py test

%install
%py3_install

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.4.40-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.4.40-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.4.40-1
- Automatic Version Bump
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 1.3.20-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 1.3.19-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.3.18-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 1.2.11-3
- Build with python3
- Mass removal python2
* Thu Jan 10 2019 Alexey Makhalov <amakhalov@vmware.com> 1.2.11-2
- Added BuildRequires python2-devel
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.2.11-1
- Update to version 1.2.11
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.1.7-2
- Use python2 explicitly
* Thu Mar 30 2017 Siju Maliakkal <smaliakal@vmware.com> 1.1.7-1
- Updating package version to latest
* Fri Nov 18 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0.15-2
- Remove noarch
* Tue Sep 6 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.15-1
- Initial packaging for Photon
