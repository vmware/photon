Summary:        Python NTP library
Name:           python3-ntplib
Version:        0.3.4
Release:        3%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/ntplib/

Source0:        ntplib-%{version}.tar.gz
%define         sha512 ntplib=368852f3fcc9e9a1c90340656bcf8e9b1143d62f616a1f177567eed419125466d572e57bac9a25465c775499cfb6b5ce1b1ee9a93c54e93667d751285757709e

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
This module offers a simple interface to query NTP servers from Python.

It also provides utility functions to translate NTP fields values to text (mode, leap indicator…). Since it’s pure Python, and only depends on core modules, it should work on any platform with a Python implementation.

%prep
%autosetup -p1 -n ntplib-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

#%%check
#Commented out %check due to no test existence

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Mon Aug 26 2024 Prashant S Chauhan <prashant.singh-chauha@broadcom.com> 0.3.4-3
- Remove python3-incremental from BuildRequires
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.3.4-2
- Bump up to compile with python 3.10
* Wed Oct 14 2020 Tapas Kundu <tkundu@vmware.com> 0.3.4-1
- Update to 0.3.4
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 0.3.3-3
- Mass removal python2
* Wed Jul 05 2017 Chang Lee <changlee@vmware.com> 0.3.3-2
- Removed %check due to no test existence.
* Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 0.3.3-1
- Initial packaging for Photon.
