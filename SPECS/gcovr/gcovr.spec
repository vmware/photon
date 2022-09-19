Summary:	The gcovr command provides a utility for managing the use of the GNU gcov utility
Name:		gcovr
Version:	4.2
Release:	4%{?dist}
License:	BSD Clause-3
URL:		http://gcovr.com/
Source0:	https://github.com/gcovr/gcovr/archive/%{name}-%{version}.tar.gz
%define sha512 gcovr=bf9e22a58b8390eca391dc8f6ba58c4ca0765e66f18ac6f8d8f80609411df2bab74a846eb179a1aded81b7774fa8a8121bb2d586556aeaf43fd729205b0d0c72
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildRequires:  python3-devel
BuildRequires:	python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-six
BuildRequires:  python3-attrs
%endif
Requires:       python3
Requires:       python3-libs
Buildarch:	noarch
%description
The gcovr command provides a utility for managing the use of the GNU gcov utility and generating summarized code coverage results. This command is inspired by the Python coverage.py package, which provides a similar utility in Python. Gcovr produces either compact human-readable summary reports, machine readable XML reports or a simple HTML summary.

%prep
%autosetup

%build
%py3_build

%install
%py3_install
mv %{buildroot}/%{_bindir}/gcovr  %{buildroot}/%{_bindir}/gcovr3

%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 funcsigs pathlib2 pluggy utils atomicwrites more_itertools iniconfig
$easy_install_3 pyutilib
python3 setup.py test

%files
%defattr(-,root,root)
%doc README.rst LICENSE.txt CHANGELOG.rst
%{_bindir}/gcovr3
%{python3_sitelib}*

%changelog
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
