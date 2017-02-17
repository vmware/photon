%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-enum
Version:        0.4.6
Release:        1%{?dist}
Summary:        Robust enumerated type support in Python
License:        MIT
Group:          Development/Languages/Python
Url:            http://pypi.python.org/packages/source/e/enum/enum-%{version}.tar.gz
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:        enum-%{version}.tar.gz
%define sha1    enum=b8868b1370181e92bbffbcd18b3ccd2be1f0438d

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
This package provides a module for robust enumerations in Python. 

%prep
%setup -n enum-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python setup.py test

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%changelog
*   Thu Feb 16 2017 Xiaolin Li <xiaolinl@vmware.com> 0.4.6-1
-   Initial packaging for Photon
