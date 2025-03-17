Name:           python3-hatchling
Version:        1.11.1
Release:        2%{?dist}
Summary:        The build backend used by Hatch
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/hatchling/
Source0:        https://files.pythonhosted.org/packages/source/h/hatchling/hatchling-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.11.1-2
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.11.1-1
- Initial version
