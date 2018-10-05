%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        A port of the caching algorithms in httplib2 for use with requests session object.
Name:           python-CacheControl
Version:        0.12.5
Release:        1%{?dist}
License:        Apache Software License
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/ionrock/cachecontrol/archive/v%{version}.tar.gz
Source0:        CacheControl-%{version}.tar.gz
%define sha1    CacheControl=ccc7d5ff074b5c1a5ea96db1fcd322e9d2f67668

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python-requests
Requires:       python-msgpack
BuildArch:      noarch

%description
CacheControl is a port of the caching algorithms in httplib2 for use with requests session object.

It was written because httplib2's better support for caching is often mitigated by its lack of threadsafety. The same is true of requests in terms of caching.

%package -n     python3-CacheControl
Summary:        Python3 CacheControl
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3-requests
Requires:       python3-msgpack

%description -n python3-CacheControl

%prep
%setup -q -n CacheControl-%{version}
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
mv %{buildroot}/%{_bindir}/doesitcache %{buildroot}/%{_bindir}/doesitcache3
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*
%{_bindir}/doesitcache

%files -n python3-CacheControl
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/doesitcache3

%changelog
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.12.5-1
-   Update to version 0.12.5
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.12.3-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu May 25 2017 Xiaolin Li <xiaolinl@vmware.com> 0.12.3-1
-   Initial version
