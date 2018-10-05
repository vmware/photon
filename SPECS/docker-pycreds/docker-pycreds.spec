%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           docker-pycreds
Version:        0.3.0
Release:        1%{?dist}
Summary:        Python API for docker credentials store
License:        ASL2.0
Group:          Development/Languages/Python
URL:            https://pypi.python.org/packages/95/2e/3c99b8707a397153bc78870eb140c580628d7897276960da25d8a83c4719/%{name}-%{version}.tar.gz
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha1    docker-pycreds=f6f9d96037a3befc7b5647f9bc09882bc130e52d

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
Python API for docker credentials store

%package -n     docker-pycreds3
Summary:        Python3 API for docker credentials store

%description -n docker-pycreds3
Python3 API for docker credentials store

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

%files -n docker-pycreds3
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Tue Sep 04 2018 Tapas Kundu <tkundu@vmware.com> 0.3.0-1
-   Upgraded to 0.3.0 version
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.2.1-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Sun Jun 04 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.2.1-1
-   Initial version of docker-pycreds for PhotonOS.
