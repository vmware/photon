Name:           python3-pathspec
Version:        0.10.1
Release:        2%{?dist}
Summary:        The build backend used by Hatch
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/pathspec
Source0:        https://files.pythonhosted.org/packages/source/p/pathspec/pathspec-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

Requires:       python3

%description
pathspec is a utility library for pattern matching of file paths.

%prep
%autosetup -n pathspec-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
python3 setup.py test

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.10.1-2
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.10.1-1
- Initial version
