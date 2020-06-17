%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Incremental is a small library that versions your Python projects.
Name:           python3-incremental
Version:        17.5.0
Release:        2%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/incremental
Source0:        incremental-%{version}.tar.gz
%define sha1    incremental=ec60b72cf95a092931f1e83807f5d641d80ae924

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
Incremental is a small library that versions your Python projects.

%prep
%setup -q -n incremental-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 17.5.0-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 17.5.0-1
-   Update to version 17.5.0
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 16.10.1-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 16.10.1-1
-   Initial packaging for Photon.
