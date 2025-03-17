Summary:        Python NTP library
Name:           python3-ntplib
Version:        0.4.0
Release:        3%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/ntplib/

Source0:        ntplib-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-incremental

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
This module offers a simple interface to query NTP servers from Python.

It also provides utility functions to translate NTP fields values to text (mode, leap indicator…). Since it’s pure Python, and only depends on core modules, it should work on any platform with a Python implementation.

%prep
%autosetup -p1 -n ntplib-%{version}

%build
%py3_build

%install
%py3_install

#%%check
#Commented out %check due to no test existence

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.4.0-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.4.0-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.4.0-1
- Automatic Version Bump
* Wed Oct 14 2020 Tapas Kundu <tkundu@vmware.com> 0.3.4-1
- Update to 0.3.4
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 0.3.3-3
- Mass removal python2
* Wed Jul 05 2017 Chang Lee <changlee@vmware.com> 0.3.3-2
- Removed %check due to no test existence.
* Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 0.3.3-1
- Initial packaging for Photon.
