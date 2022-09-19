Name:           python3-hatchling
Version:        1.11.1
Release:        1%{?dist}
Summary:        The build backend used by Hatch
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/hatchling/
Source0:        https://files.pythonhosted.org/packages/source/h/hatchling/hatchling-%{version}.tar.gz
%define sha512  hatchling=3ff9d41517eb2ebb8a3fab2d57e7430800650209e3253171cc96f83c4dc62441b82f3a69626566c795932df857d1c31dbb32b5a447324f83136aa9163fde540e
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-pip
BuildRequires:  python3-pathspec
BuildRequires:  python3-packaging
BuildRequires:  python3-pluggy

Requires:       python3

Provides:       python3dist(hatchling) = %{version}-%{release}

%description
This is the extensible, standards compliant build backend used by Hatch.

%prep
%autosetup -n hatchling-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
python3 setup.py test

%files
%defattr(-,root,root)
%{_bindir}/hatchling
%{python3_sitelib}/*

%changelog
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.11.1-1
- Initial version
