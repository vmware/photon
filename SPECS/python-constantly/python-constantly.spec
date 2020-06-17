%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Symbolic constants in Python.
Name:           python3-constantly
Version:        15.1.0
Release:        3%{?dist}
Url:            https://pypi.python.org/pypi/constantly
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        constantly-%{version}.tar.gz
%define sha1    constantly=02e60c17889d029e48a52a74259462e087a3dcdd

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description
A library that provides symbolic constant support. It includes collections and constants with text, numeric, and bit flag values. Originally twisted.python.constants from the Twisted project.


%prep
%setup -q -n constantly-%{version}

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
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 15.1.0-3
-   Mass removal python2
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 15.1.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 15.1.0-1
-   Initial packaging for Photon
