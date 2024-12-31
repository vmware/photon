Name:           python3-virtualenv
Version:        20.1.0
Release:        4%{?dist}
Summary:        Virtual Python Environment builder
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/virtualenv
Source0:        virtualenv-%{version}.tar.gz
Patch0:         CVE-2024-53899.patch

%define sha512  virtualenv=740bf8ba30d836c240d248dd2fa31a8702cfa8f96a6192dd6430dbeff3ebbf0fe67d4fd2439ed4961869731520b097783a29381eae3f81f6700b6050b75422c8
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3
BuildRequires:  python3-appdirs
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  curl-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-macros
Requires:       python3
Requires:       python3-libs
Requires:       python3-appdirs
Requires:       python3-distlib
Requires:       python3-filelock
Requires:       python3-setuptools
Requires:       python3-six

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-filelock
BuildRequires: python3-coverage
BuildRequires: python3-distlib
%endif

BuildArch:      noarch

%description
virtualenv is a tool to create isolated Python environment.

%prep
%autosetup -p1 -n virtualenv-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
pip3 install tomli flaky pytest-mock pytest-freezer
%pytest -k "not test_py_pyc_missing and not test_py_info_setuptools"

%files
%defattr(-,root,root,-)
%{_bindir}/virtualenv
%{python3_sitelib}/*

%changelog
* Tue Dec 31 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 20.1.0-4
- Fix CVE-2024-53899
* Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 20.1.0-3
- Add python3-pip as BuildRequires to build with python3.10
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 20.1.0-2
- Fix build with new rpm
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 20.1.0-1
- Automatic Version Bump
* Thu Oct 01 2020 Gerrit Photon <photon-checkins@vmware.com> 20.0.32-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 20.0.31-1
- Automatic Version Bump
* Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 20.0.30-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 20.0.28-1
- Automatic Version Bump
* Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 16.0.0-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 16.0.0-1
- Update to version 16.0.0
* Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 15.1.0-1
- Initial version of python-virtualenv package for Photon.
