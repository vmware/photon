%global build_if %{photon_subrelease} >= 92

%global srcname pyproject_metadata

Summary:        PEP 621 metadata parsing
Name:           python3-pyproject-metadata
Version:        0.11.0
Release:        1%{?dist}
Url:            https://pypi.org/project/pyproject-metadata/
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/83/fa/8bf4fa41adfebd95dce360afe3f5fca243a17932089d3d5486e95ca44c57/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-packaging
BuildRequires:  python3-flit-core
Requires:       python3

%description
Given a Python data structure representing pyproject.toml [project] metadata (already parsed),
it will validate this input and generate a PEP 643-compliant metadata file.

%prep
%autosetup -n pyproject_metadata-%{version}

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
* Tue Dec 09 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.11.0-1
- Initial packaging for Photon
