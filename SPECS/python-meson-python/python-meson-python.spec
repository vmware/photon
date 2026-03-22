%global build_if %{photon_subrelease} >= 92

%global srcname meson_python

Summary:        Meson PEP 517 Python build backend
Name:           python3-meson-python
Version:        0.19.0
Release:        1%{?dist}
Url:            https://pypi.org/project/meson-python/
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/32/98/7fe5d1bf741c03c6eea04b6245737dbd79657d4f9200e82fcbb4cc12637b/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-packaging
BuildRequires:  python3-pyproject-metadata
BuildRequires:  meson
Requires:       python3
Requires:       python3-packaging
Requires:       python3-pyproject-metadata

%description
meson-python is a Python build back-end built on top of the Meson build system.
It enables using Meson for the configuration and build steps of Python packages.

%prep
%autosetup -n %{srcname}-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Thu Feb 12 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.19.0-1
- Initial packaging for Photon
