Summary:    The gcovr command provides a utility for managing the use of the GNU gcov utility
Name:       gcovr
Version:    5.2
Release:    3%{?dist}
URL:        http://gcovr.com
Vendor:     VMware, Inc.
Group:      Development/Tools
Distribution:   Photon

Source0: https://github.com/gcovr/gcovr/archive/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-setuptools

%if 0%{?with_check}
BuildRequires: openssl-devel
BuildRequires: curl-devel
BuildRequires: python3-six
BuildRequires: python3-attrs
BuildRequires: python3-lxml
BuildRequires: python3-pip
%endif

Requires: python3
Requires: python3-lxml

Buildarch: noarch

%description
The gcovr command provides a utility for managing the use of the GNU gcov utility and generating summarized code coverage results. This command is inspired by the Python coverage.py package, which provides a similar utility in Python. Gcovr produces either compact human-readable summary reports, machine readable XML reports or a simple HTML summary.

%prep
%autosetup -p1

%build
%{py3_build}

%install
%{py3_install}
mv %{buildroot}%{_bindir}/gcovr %{buildroot}%{_bindir}/gcovr3
ln -sv gcovr3 %{buildroot}%{_bindir}/gcovr

%if 0%{?with_check}
%check
pip3 install nox
python3 -m nox
%endif

%files
%defattr(-,root,root)
%doc README.rst LICENSE.txt CHANGELOG.rst
%{_bindir}/gcovr*
%{python3_sitelib}*

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.2-3
- Release bump for SRP compliance
* Fri Aug 04 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.2-2
- Fix requires
* Mon Dec 05 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.2-1
- Update to v5.2
* Mon Nov 28 2022 Prashant S Chauhan <psinghchauha@vmware.com> 4.2-4
- Update release to compile with python 3.11
* Mon Nov 16 2020 Prashant S Chauhan <psinghchauha@vmware.com> 4.2-3
- Fix makecheck, install missing iniconfig module
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.2-2
- openssl 1.1.1
* Wed Jul 29 2020 Gerrit Photon <photon-checkins@vmware.com> 4.2-1
- Automatic Version Bump
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 4.1-4
- Mass removal python2
* Wed Sep 18 2019 Prashant Singh Chauhan <psinghchauha@vmware.com> 4.1-3
- Fix for make check failure using pip instead of easy_install for python2
* Wed Nov 21 2018 Ashwin H <ashwinh@vmware.com> 4.1-2
- Fix gcovr %check
* Tue Sep 18 2018 Sujay G <gsujay@vmware.com> 4.1-1
- Bump gcovr version to 4.1
* Fri Jun 09 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.3-1
- Initial build. First version
