%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           docker-py
Version:        2.3.0
Release:        2%{?dist}
Summary:        Python API for docker
License:        ASL2.0
Group:          Development/Languages/Python
Url:            https://github.com/docker/docker-py
Source0:        %{name}-%{version}.tar.gz
%define sha1    docker-py=9029528629fd0c5ebe3132acfbcb078247a905ba

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-ipaddress
BuildRequires:  python-pip
BuildRequires:  python-requests
BuildRequires:  python-setuptools
BuildRequires:  python-six
BuildRequires:  python-xml
Requires:       python2
Requires:       python2-libs
Requires:       docker-pycreds
Requires:       python-backports.ssl_match_hostname
Requires:       python-ipaddress
Requires:       python-requests
Requires:       python-six
Requires:       python-websocket-client

BuildArch:      noarch

%description
Python API for docker

%package -n     docker-py3
Summary:        Python3 API for docker
BuildRequires:  python3-devel

Requires:       python3
Requires:       python3-libs
Requires:       docker-pycreds3
Requires:       python3-requests
Requires:       python3-six
Requires:       python3-websocket-client

%description -n docker-py3
Python3 API for docker

%prep
%setup -n %{name}-%{version}
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

%files -n docker-py3
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Dec 01 2017 Xiaolin Li <xiaolinl@vmware.com> 2.3.0-2
-   Added docker-pycreds3, python3-requests, python3-six,
-   python3-websocket-client to requires of docker-py3
*   Sun Jun 04 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.3.0-1
-   Initial version of docker-py for PhotonOS.
