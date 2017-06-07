%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        This library brings the updated configparser from Python 3.5 to Python 2.6-3.5.
Name:           python-configparser
Version:        3.5.0
Release:        2%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/configparser
Source0:        configparser-%{version}.tar.gz
%define sha1    configparser=8ee6b29c6a11977c0e094da1d4f5f71e7e7ac78b

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
The ancient ConfigParser module available in the standard library 2.x has seen a major update in Python 3.2. This is a backport of those changes so that they can be used directly in Python 2.6 - 3.5.

%package -n     python3-configparser
Summary:        python-configparser
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-configparser
Python 3 version.

%prep
%setup -q -n configparser-%{version}

%build
python setup.py build
python3 setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install py
python setup.py test
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%files -n python3-configparser
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.0-1
-   Initial packaging for Photon
