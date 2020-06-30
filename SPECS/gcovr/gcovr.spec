%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:	The gcovr command provides a utility for managing the use of the GNU gcov utility
Name:		gcovr
Version:	4.2
Release:	1%{?dist}
License:	BSD Clause-3
URL:		http://gcovr.com/
Source0:	https://github.com/gcovr/gcovr/archive/%{name}-%{version}.tar.gz
%define sha1 gcovr=3094f90ed0ca30eb3aa0a9b1b236d9cff1279600
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildRequires:  python3-devel
BuildRequires:  python3
BuildRequires:  python3-libs
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
%setup -q

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/gcovr  %{buildroot}/%{_bindir}/gcovr3


%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 funcsigs pathlib2 pluggy utils atomicwrites more_itertools
$easy_install_3 pyutilib
python3 setup.py test

%files
%defattr(-,root,root)
%doc README.rst LICENSE.txt CHANGELOG.rst
%{_bindir}/gcovr3
%{python3_sitelib}*

%changelog
*   Tue Jul 29 2020 Gerrit Photon <photon-checkins@vmware.com> 4.2-1
-   Automatic Version Bump
*   Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 4.1-4
-   Mass removal python2
*   Wed Sep 18 2019 Prashant Singh Chauhan <psinghchauha@vmware.com> 4.1-3
-   Fix for make check failure using pip instead of easy_install for python2
*   Wed Nov 21 2018 Ashwin H <ashwinh@vmware.com> 4.1-2
-   Fix gcovr %check
*   Tue Sep 18 2018 Sujay G <gsujay@vmware.com> 4.1-1
-   Bump gcovr version to 4.1
*   Fri Jun 09 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.3-1
-   Initial build. First version
