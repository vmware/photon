%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-ipaddress
Version:        1.0.22
Release:        3%{?dist}
Summary:        Port of the 3.3+ ipaddress module to 2.6, 2.7, 3.2
License:        Python Software Foundation License (Python Software Foundation License)
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/ipaddress
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:        ipaddress-%{version}.tar.gz
%define sha1    ipaddress=7b60cef3c7fdb7fa9c991ddff5968754cec6adb0

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
IPv4/IPv6 manipulation library

%prep
%setup -n ipaddress-%{version}

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
*   Wed Jun 17 2020 Tapas Kundu <tkundu@vmware.com> 1.0.22-3
-   Mass removal python2
*   Thu Sep 13 2018 Tapas Kundu <tkundu@vmware.com> 1.0.22-2
-   Updated the license
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.0.22-1
-   Update to version 1.0.22
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.0.18-2
-   Change python to python2
*   Thu Feb 16 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0.18-1
-   Initial packaging for Photon
