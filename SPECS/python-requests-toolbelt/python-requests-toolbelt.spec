%define srcname requests-toolbelt

Name:           python3-requests-toolbelt
Version:        0.10.1
Release:        3%{?dist}
Summary:        Utility belt for advanced users of python-requests
Group:          Development/Languages/Python
URL:            https://toolbelt.readthedocs.io
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/0c/4c/07f01c6ac44f7784fa399137fbc8d0cdc1b5d35304e8c0f278ad82105b58/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=e4dfc58bd9d84f3590582853345602ba4e0dcb292733cc3c5d92057f5fd1d414bc1058d06d3c825d6f9eb802281592515f24473c6e8a59c91eb8836ad31e45d7

Source1: license.txt
%include %{SOURCE1}

%if 0%{?with_check}
BuildRequires: python3-pip
BuildRequires: python3-pytest
BuildRequires: python3-pluggy
BuildRequires: python3-more-itertools
%endif

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pyOpenSSL
BuildRequires: python3-requests

Requires: python3-requests

BuildArch: noarch

%description
This is just a collection of utilities for python-requests, but don’t really\
belong in requests proper.

%prep
%autosetup -p1 -n requests-toolbelt-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
pip3 install betamax
python3 -m pytest -v --ignore=tests/test_x509_adapter.py
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{python3_sitelib}/requests_toolbelt/
%{python3_sitelib}/requests_toolbelt-*.egg-info/

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.10.1-3
- Release bump for SRP compliance
* Tue Dec 26 2023 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.10.1-2
- Bump up as part of python3-pyOpenSSL update
* Thu Aug 25 2022 Mukul Sikka <msikka@vmware.com> 0.10.1-1
- Initial version of python-requests-toolbelt package for Photon.
