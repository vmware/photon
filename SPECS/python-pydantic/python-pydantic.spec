Summary:        Data validation using Python type hinting
Name:           python3-pydantic
Version:        1.10.1
Release:        3%{?dist}
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/pydantic

Source0:        https://files.pythonhosted.org/packages/d5/eb/d5ee9e58b2a4608c320fc72e5d471ba0cd949e8ef6f2689d30d1bd782d9f/pydantic-1.10.1.tar.gz

Source1: license.txt
%include %{SOURCE1}
Patch0: CVE-2024-3772.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_check}
BuildRequires:  python3-pip
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
# Remove bundled egg-info
rm -rf pydantic.egg-info

%build
%py3_build

%install
%py3_install

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
%{python3_sitelib}/pydantic
%{python3_sitelib}/pydantic-%{version}-py%{python3_version}.egg-info

%changelog
* Tue Apr 22 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.10.1-3
- Fix CVE-2024-3772
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.10.1-2
- Release bump for SRP compliance
* Wed Oct 12 2022 Nitesh Kumar <kunitesh@vmware.com> 1.10.1-1
- Initial version
