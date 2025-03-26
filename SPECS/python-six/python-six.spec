Name:           python3-six
Version:        1.16.0
Release:        2%{?dist}
Summary:        Python 2 and 3 compatibility utilities
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Languages/Python
Url:            https://pypi.org/project/six
Source0:        https://pypi.python.org/packages/source/s/six/six-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if 0%{?with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
%endif
Requires:       python3
Requires:       python3-libs
Provides:       python%{python3_version}dist(six)
BuildArch:      noarch

%description
Six is a Python 2 and 3 compatibility library. It provides utility functions for smoothing over the differences between the Python versions with the goal of writing Python code that is compatible on both Python versions.

%prep
%autosetup -n six-%{version}

%build
%py3_build

%install
%py3_install

%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pytest
python3 test_six.py

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.16.0-2
- Release bump for SRP compliance
* Mon Oct 10 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.16.0-1
- Update release to compile with python 3.11
* Wed Jul 21 2021 Tapas Kundu <tkundu@vmware.com> 1.15.0-3
- Added provides
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.15.0-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.15.0-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 1.11.0-3
- Mass removal python2
* Mon Nov 26 2018 Tapas Kundu <tkundu@vmware.com> 1.11.0-2
- Fix makecheck
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.11.0-1
- Update to version 1.11.0
* Fri Jun 23 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.10.0-8
- Add python-setuptools to BuildRequires to avoid Update issues
* Wed Jun 21 2017 Xiaolin Li <xiaolinl@vmware.com> 1.10.0-7
- Fix make check.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.10.0-6
- Use python2 explicitly
* Wed Apr 05 2017 Sarah Choi <sarahc@vmware.com> 1.10.0-5
- Remove python-setuptools from BuildRequires
* Mon Jan 09 2017 Xiaolin Li <xiaolinl@vmware.com> 1.10.0-4
- Added python3 site-packages.
* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 1.10.0-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.10.0-2
- GA - Bump release of all rpms
* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.10.0-1
- Upgrade version
* Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
