%global build_if %{photon_subrelease} >= 92

%global debug_package %{nil}
%define srcname sqlalchemy

Summary:        The Python SQL Toolkit and Object Relational Mapper
Name:           python3-sqlalchemy
Version:        2.0.48
Release:        2%{?dist}
Url:            http://www.sqlalchemy.org
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/54/55/a475df74f583b4ceeefd5a121fd28045af54efe204863de1e3b154385674/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

Requires:       python3
Requires:       python3-typing-extensions

%description
SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. SQLAlchemy provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.

%prep
%autosetup -n %{srcname}-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
pip3 install tox
tox -e py311-sqlite

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Mon Mar 23 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.48-2
- Fix config.yaml
* Sun Mar 22 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.48-1
- Version upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.0.0-1
- Update to 2.0.0, fixes PVE-2022-51668
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
