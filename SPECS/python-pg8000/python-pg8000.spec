%global debug_package %{nil}
%define srcname pg8000

Name:           python3-pg8000
Version:        1.31.2
Release:        1%{?dist}
Summary:        A Pure-Python PostgreSQL Driver
URL:            http://pgaudit.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/0f/d7/0554640cbe3e193184796bedb6de23f797c03958425176faf0e694c06eb0/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-hatchling
BuildRequires:  python3-pathspec
BuildRequires:  python3-pluggy
BuildRequires:  python3-versioningit
BuildRequires:  python3-packaging

Requires: python3
Requires: python3-dateutil
Requires: python3-scramp

%description
pg8000 is a pure-Python PostgreSQL driver that complies with DB-API 2.0.
pg8000 comes with two APIs, the native pg8000 API and the DB-API 2.0 standard API.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Fri Aug 29 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.31.2-1
- Initial build
