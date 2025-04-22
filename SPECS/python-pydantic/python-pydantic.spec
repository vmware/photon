Summary:        Data validation using Python type hinting
Name:           python3-pydantic
Version:        1.10.1
Release:        2%{?dist}
Group:          Development/Tools
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/pydantic

Source0:        https://files.pythonhosted.org/packages/d5/eb/d5ee9e58b2a4608c320fc72e5d471ba0cd949e8ef6f2689d30d1bd782d9f/pydantic-1.10.1.tar.gz
%define sha512  pydantic=e0394b90c39fd5294b7f4f280548d07113d771737943c390405d5bdbaf05216dc20c6adb7860cbbe1f8ee9698909447e72a8a5245009c710fe9b172d53bb2260
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
%pytest -v
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
* Tue Apr 22 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.10.1-2
- Fix CVE-2024-3772
* Wed Oct 12 2022 Nitesh Kumar <kunitesh@vmware.com> 1.10.1-1
- Initial version
