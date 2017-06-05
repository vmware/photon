%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-enum
Version:        0.4.6
Release:        2%{?dist}
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
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%changelog
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.4.6-2
-   Changed python to python2
*   Thu Feb 16 2017 Xiaolin Li <xiaolinl@vmware.com> 0.4.6-1
-   Initial packaging for Photon
