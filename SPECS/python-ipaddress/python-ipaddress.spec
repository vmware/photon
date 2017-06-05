%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-ipaddress
Version:        1.0.18
Release:        2%{?dist}
Summary:        Port of the 3.3+ ipaddress module to 2.6, 2.7, 3.2
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/ipaddress
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:        ipaddress-%{version}.tar.gz
%define sha1    ipaddress=f15a3714e4bea2ddfe54e80ad6f7b5de57cc94c5

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
IPv4/IPv6 manipulation library

%prep
%setup -n ipaddress-%{version}

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
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.0.18-2
-   Change python to python2
*   Thu Feb 16 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0.18-1
-   Initial packaging for Photon
