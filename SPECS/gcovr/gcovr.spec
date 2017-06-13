%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:	The gcovr command provides a utility for managing the use of the GNU gcov utility
Name:		gcovr
Version:	3.3
Release:	1%{?dist}
License:	BSD Clause-3
URL:		http://gcovr.com/
Source0:	https://github.com/gcovr/gcovr/archive/%{name}-%{version}.tar.gz
%define sha1 gcovr=880f1497859e83a45572914067a3a0ccae964ad5
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs
Buildarch:	noarch
%description
The gcovr command provides a utility for managing the use of the GNU gcov utility and generating summarized code coverage results. This command is inspired by the Python coverage.py package, which provides a similar utility in Python. Gcovr produces either compact human-readable summary reports, machine readable XML reports or a simple HTML summary.

%package -n     python3-gcovr
Summary:        python3-gcovr
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs
%description -n python3-gcovr

%prep
%setup -q

%build
python2 setup.py build
python3 setup.py build

%install
python2 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
python3 setup.py test

%files
%defattr(-,root,root)
%doc README.md LICENSE.txt CHANGELOG.txt
%{_bindir}
%{python2_sitelib}*

%files -n python3-gcovr
%defattr(-,root,root)
%doc README.md LICENSE.txt CHANGELOG.txt
%{python3_sitelib}*

%changelog
*   Fri Jun 09 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.3-1
-   Initial build. First version
