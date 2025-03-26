Summary:        This library brings the updated configparser from Python 3.5 to Python 2.6-3.5.
Name:           python3-configparser
Version:        5.3.0
Release:        2%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/configparser
Source0:        configparser-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-packaging
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-devel
BuildRequires:  curl-devel
BuildRequires:  python3-setuptools_scm
Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
The ancient ConfigParser module available in the standard library 2.x has seen a major update in Python 3.2. This is a backport of those changes so that they can be used directly in Python 2.6 - 3.5.

%prep
%autosetup -p1 -n configparser-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 py
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.3.0-2
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 5.3.0-1
- Update to 5.3.0
* Sun Aug 29 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.0.1-3
- Add python3-setuptools_scm as BuildRequires to fix 'toml' build failure
* Thu Feb 18 2021 Prashant S Chauhan <psinghchauha@vmware.com> 5.0.1-2
- Fix make check
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 5.0.1-1
- Automatic Version Bump
* Wed Oct 28 2020 Dweep Advani <dadvani@vmware.com> 5.0.0-2
- Fixed install conflicts with python-backports.ssl_match_hostname
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 5.0.0-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 3.5.0-4
- Removed python2
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.0-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.5.0-2
- Changed python to python2
* Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.0-1
- Initial packaging for Photon
