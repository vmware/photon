%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-websocket-client
Version:        0.7.0
Release:        1%{?dist}
Summary:        WebSocket client for python
License:        LGPL
Group:          Development/Languages/Python
Url:            https://pypi.python.org/packages/8f/2d/8eb061e94e29c0b35e1fd87f1c0e779f4288d7393b180ef0e5c0ee2b155e/websocket-client-%{version}.tar.gz
Source0:        websocket-client-%{version}.tar.gz
%define sha1    websocket-client=cb36dc1c9b0dda4d4672f0d2c812e65343f509b8

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
WebSocket client for python

%package -n     python3-websocket-client
Summary:        WebSocket client for python3
BuildRequires:  python3-devel

%description -n python3-websocket-client
WebSocket client for python3

%prep
%setup -n websocket-client-%{version}
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
*   Sun Jun 04 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.7.0-1
-   Initial version of python WebSocket for PhotonOS.
