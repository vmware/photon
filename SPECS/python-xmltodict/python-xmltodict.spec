%global pypi_name xmltodict

Summary:       Python to transform XML to JSON
Name:          python3-%{pypi_name}
Version:       0.13.0
Release:       1%{?dist}
License:       MIT
URL:           https://github.com/martinblech/%{pypi_name}
Group:         Development/Languages/Python
Vendor:        VMware, Inc.
Distribution:  Photon
BuildArch:     noarch

Source0: https://github.com/martinblech/%{pypi_name}/archive/refs/tags/%{pypi_name}-%{version}.tar.gz
%define sha512 %{pypi_name}=a7c12efa3c8d9b30a36a4b0ed2a8215f9833728d7988e74ef36458790a786c4c7517e536e8a82939623069716cdff258da5aab378a74f884a0fa245e7951f0bf

BuildRequires: python3-devel
BuildRequires: python3-setuptools

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
%{py3_build}

%install
%{py3_install}
rm -rf %{buildroot}/%{python3_sitelib}/__pycache__/

%if 0%{?with_check}
%check
%pytest -v
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.md
%license LICENSE
%{python3_sitelib}/%{pypi_name}.py
%{python3_sitelib}/%{pypi_name}-%{version}-*

%changelog
* Sat Oct 14 2023 Oliver Kurth <okurth@vmware.com> 0.13.0-1
- Initial build
