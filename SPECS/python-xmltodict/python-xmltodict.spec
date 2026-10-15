%global build_if %{photon_subrelease} >= 92

%global pypi_name xmltodict

Summary:       Python to transform XML to JSON
Name:          python3-%{pypi_name}
Version:       1.0.4
Release:       1%{?dist}
URL:           https://github.com/martinblech/%{pypi_name}
Group:         Development/Languages/Python
Vendor:        VMware, Inc.
Distribution:  Photon
BuildArch:     noarch

Source0: https://github.com/martinblech/%{pypi_name}/archive/refs/tags/v%{version}.tar.gz#/%{pypi_name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-build
BuildRequires: python3-installer
BuildRequires: python3-packaging

Requires: python3
Requires: python3-xml

%if 0%{?with_check}
BuildRequires: python3-pytest
%endif

%description
Python module that makes working with XML feel like you are working with JSON

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
%pytest -v
%endif

%clean
rm -rf %{buildroot}

%files -f %{py_ghost_filelist}
%defattr(-,root,root)
%doc README.md
%license LICENSE
%{python3_sitelib}/%{pypi_name}.py
%{python3_sitelib}/%{pypi_name}-%{version}.dist-info

%changelog
* Thu Oct 15 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.0.4-1
- Upgrade to 1.0.4
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.13.0-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.13.0-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.13.0-2
- Release bump for SRP compliance
* Sat Oct 14 2023 Oliver Kurth <okurth@vmware.com> 0.13.0-1
- Initial build
