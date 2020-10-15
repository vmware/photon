%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           docker-pycreds3
Version:        0.4.0
Release:        1%{?dist}
Summary:        Python API for docker credentials store
License:        ASL2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://files.pythonhosted.org/packages/c5/e6/d1f6c00b7221e2d7c4b470132c931325c8b22c51ca62417e300f5ce16009/docker-pycreds-%{version}.tar.gz
Source0:        docker-pycreds-%{version}.tar.gz
%define sha1    docker-pycreds=36a0e5d70f0a237e2bbd3f87dbd3e60a4e486d53

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
*   Thu Oct 15 2020 Ashwin H <ashwinh@vmware.com> 0.4.0-1
-   Upgrade to 0.4.0 release.
*   Thu Jun 18 2020 Tapas Kundu <tkundu@vmware.com> 0.3.0-2
=   Mass removal python2
*   Tue Sep 04 2018 Tapas Kundu <tkundu@vmware.com> 0.3.0-1
-   Upgraded to 0.3.0 version
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.2.1-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Sun Jun 04 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.2.1-1
-   Initial version of docker-pycreds for PhotonOS.
