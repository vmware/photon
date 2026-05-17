%global build_if %{photon_subrelease} >= 91

Summary:        Data validation using Python type hinting
Name:           python3-pydantic
Version:        1.10.26
Release:        2%{?dist}
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/pydantic

BuildArch:      noarch

Source0: pydantic-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip

%if 0%{?with_check}
BuildRequires:  python3-typing-extensions
BuildRequires:  python3-pytest
%endif

Requires:       python3-email-validator
Requires:       python3-ujson
Requires:       python3-typing-extensions

%description
Data validation and settings management using python type hinting.

%prep
%autosetup -p1 -n pydantic-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%if 0%{?with_check}
%check
pip3 install pytest-mock
%pytest -v -k "not test_partial_legacy_typeddict"
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.10.26-2
- Extended to build for subrelease 91 and above
* Sun Mar 22 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.10.26-1
- Version upgrade
* Tue Apr 22 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.10.1-3
- Fix CVE-2024-3772
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.10.1-2
- Release bump for SRP compliance
* Wed Oct 12 2022 Nitesh Kumar <kunitesh@vmware.com> 1.10.1-1
- Initial version
