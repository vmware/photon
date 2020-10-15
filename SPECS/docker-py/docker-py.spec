%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           docker-py3
Version:        4.3.1
Release:        1%{?dist}
Summary:        Python API for docker
License:        ASL2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/docker/docker-py
Source0:        docker-py-%{version}.tar.gz
%define sha1    docker-py=eed3cb687f8103dd8679c672e64251b7b3bfd337

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-ipaddress
BuildRequires:  python3-pip
BuildRequires:  python3-requests
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
Requires:       docker-pycreds3
Requires:       python3-backports.ssl_match_hostname
Requires:       python3-ipaddress
Requires:       python3-requests
Requires:       python3-six
Requires:       python3-websocket-client

BuildArch:      noarch

%description
Python API for docker


%prep
%setup -n docker-py-%{version}-release

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Thu Oct 15 2020 Ashwin H <ashwinh@vmware.com> 4.3.1-1
-   Upgrade to 4.3.1 release.
*   Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 3.5.0-2
-   Mass removal python2
*   Tue Sep 04 2018 Tapas Kundu <tkundu@vmware.com> 3.5.0-1
-   Upgraded to 3.5.0 release.
*   Fri Dec 01 2017 Xiaolin Li <xiaolinl@vmware.com> 2.3.0-3
-   Added docker-pycreds3, python3-requests, python3-six,
-   python3-websocket-client to requires of docker-py3
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.3.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Sun Jun 04 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.3.0-1
-   Initial version of docker-py for PhotonOS.
