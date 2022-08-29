%define srcname requests-toolbelt

Name:           python3-requests-toolbelt
Version:        0.9.1
Release:        1%{?dist}
Summary:        Utility belt for advanced users of python-requests
License:        ASL 2.0
Group:          Development/Languages/Python
URL:            https://toolbelt.readthedocs.io
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/sigmavirus24/requests-toolbelt/archive/%{version}/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=12667056c225ce0bc88a5959660103feed23810890abd3890ef15581aa64c09c0552c3974473e1742cbe6200bd37d6475ad34ec051e83d4fbf0a33f320dbc0cc

%if 0%{?with_check}
Patch0: python-requests-toolbelt-fix-unhandled-exception-from-tests.patch
Patch1: python-requests-toolbelt-pass-session-into-tests.patch
Patch2: python-requests-toolbelt-mock-import.patch

BuildRequires: python3-pip
BuildRequires: python3-pytest
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
%autosetup -p1 -n toolbelt-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
pip3 install betamax pluggy more_itertools
python3 -m pytest -v --ignore=tests/test_x509_adapter.py
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{python3_sitelib}/requests_toolbelt/
%{python3_sitelib}/requests_toolbelt-*.egg-info/

%changelog
* Thu Aug 25 2022 Mukul Sikka <msikka@vmware.com> 0.9.1-1
- Initial version of python-requests-toolbelt package for Photon.
