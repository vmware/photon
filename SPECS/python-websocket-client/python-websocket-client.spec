%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-websocket-client
Version:        0.53.0
Release:        1%{?dist}
Summary:        WebSocket client for python
License:        LGPL
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/websocket-client
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        websocket_client-%{version}.tar.gz
%define sha1    websocket_client=09bd8914944646fde9d2672392579a982ea0f031

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
WebSocket client for python

%package -n     python3-websocket-client
Summary:        WebSocket client for python3

%description -n python3-websocket-client
WebSocket client for python3

%prep
%setup -n websocket_client-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*
/usr/bin/wsdump.py

%files -n python3-websocket-client
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Sep 14 2018 Tapas Kundu <tkundu@vmware.com> 0.53.0-1
-   Updated to release 0.53.0
*   Thu Nov 30 2017 Xiaolin Li <xiaolinl@vmware.com> 0.44.0-1
-   Update websocket_client to version 0.44.0
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Sun Jun 04 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.7.0-1
-   Initial version of python WebSocket for PhotonOS.
