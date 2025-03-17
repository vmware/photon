%define srcname importlib_metadata

Summary:        Library to access the metadata for a Python package
Name:           python3-importlib-metadata
Version:        6.0.0
Release:        3%{?dist}
Group:          Development/Languages/Python
URL:            https://github.com/python/importlib_metadata
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/90/07/6397ad02d31bddf1841c9ad3ec30a693a3ff208e09c2ef45c9a8a5f85156/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch:     noarch

BuildRequires: python3-devel
BuildRequires: python3-packaging
BuildRequires: python3-pip
BuildRequires: python3-setuptools
BuildRequires: python3-setuptools_scm
BuildRequires: python3-wheel

%if 0%{?with_check}
BuildRequires:  python3-test
BuildRequires:  python3-pytest
BuildRequires:  python3-typing-extensions
BuildRequires:  python3-pluggy
BuildRequires:  python3-more-itertools
%endif

Requires:      python3
Requires:      python3-typing-extensions
Requires:      python3-zipp

%description
Library to access the metadata for a Python package.
This package supplies third-party access to the functionality
of importlib.metadata including improvements added to subsequent
Python versions.

%prep
%autosetup -n %{srcname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

rm -f %{buildroot}%{python3_sitelib}/typing_extensions.py

%if 0%{?with_check}
%check
pip3 install importlib_resources pyfakefs
%pytest --ignore exercises.py -k "not test_find_local"
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.0.0-3
- Release bump for SRP compliance
* Mon Jun 03 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.0.0-2
- Use system provided packages to do offline build
* Thu Jan 12 2023 Srish Srinivasan <ssrish@vmware.com> 6.0.0-1
- Initial build. First version
