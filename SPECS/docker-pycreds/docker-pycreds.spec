%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           docker-pycreds3
Version:        0.3.0
Release:        2%{?dist}
Summary:        Python API for docker credentials store
License:        ASL2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/packages/95/2e/3c99b8707a397153bc78870eb140c580628d7897276960da25d8a83c4719/docker-pycreds-%{version}.tar.gz
Source0:        docker-pycreds-%{version}.tar.gz
%define sha1    docker-pycreds=f6f9d96037a3befc7b5647f9bc09882bc130e52d

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
Python API for docker credentials store

%prep
%setup -n docker-pycreds-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Thu Jun 18 2020 Tapas Kundu <tkundu@vmware.com> 0.3.0-2
=   Mass removal python2
*   Tue Sep 04 2018 Tapas Kundu <tkundu@vmware.com> 0.3.0-1
-   Upgraded to 0.3.0 version
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.2.1-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Sun Jun 04 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.2.1-1
-   Initial version of docker-pycreds for PhotonOS.
