%global build_if %{photon_subrelease} >= 92

%define srcname requests-toolbelt

Name:           python3-requests-toolbelt
Version:        1.0.0
Release:        1%{?dist}
Summary:        Utility belt for advanced users of python-requests
Group:          Development/Languages/Python
URL:            https://toolbelt.readthedocs.io
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/requests/toolbelt/archive/refs/tags/%{version}.tar.gz#/%{srcname}-%{version}.tar.gz

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
BuildRequires: python3-build
BuildRequires: python3-installer
BuildRequires: python3-packaging
BuildRequires: python3-pyOpenSSL
BuildRequires: python3-requests

Requires: python3-requests

BuildArch: noarch

%description
This is just a collection of utilities for python-requests, but don’t really\
belong in requests proper.

%prep
%autosetup -p1 -n toolbelt-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
pip3 install betamax
python3 -m pytest -v --ignore=tests/test_x509_adapter.py
%endif

%clean
rm -rf %{buildroot}/*

%files -f %{py_ghost_filelist}
%defattr(-,root,root)
%{python3_sitelib}/requests_toolbelt/
%{python3_sitelib}/requests_toolbelt-*.dist-info/

%changelog
* Wed Oct 14 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.0.0-1
- Upgrade to 1.0.0
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.10.1-5
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.10.1-4
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.10.1-3
- Release bump for SRP compliance
* Tue Dec 26 2023 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.10.1-2
- Bump up as part of python3-pyOpenSSL update
* Thu Aug 25 2022 Mukul Sikka <msikka@vmware.com> 0.10.1-1
- Initial version of python-requests-toolbelt package for Photon.
