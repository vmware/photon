%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-websocket-client
Version:        0.53.0
Release:        3%{?dist}
Summary:        WebSocket client for python
License:        LGPL
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/websocket-client
Source0:        websocket_client-%{version}.tar.gz
%define sha1    websocket_client=09bd8914944646fde9d2672392579a982ea0f031

%if %{with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
WebSocket client for python

%prep
%setup -n websocket_client-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
/usr/bin/wsdump.py

%changelog
*   Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 0.53.0-3
-   Mass removal python2.
*   Fri Dec 07 2018 Ashwin H <ashwinh@vmware.com> 0.53.0-2
-   Add %check
*   Fri Sep 14 2018 Tapas Kundu <tkundu@vmware.com> 0.53.0-1
-   Updated to release 0.53.0
*   Thu Nov 30 2017 Xiaolin Li <xiaolinl@vmware.com> 0.44.0-1
-   Update websocket_client to version 0.44.0
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Sun Jun 04 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.7.0-1
-   Initial version of python WebSocket for PhotonOS.
