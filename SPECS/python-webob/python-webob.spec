%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        WebOb provides objects for HTTP requests and responses..
Name:           python-webob
Version:        1.8.2
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.python.org/pypi/WebOb
Source0:        https://pypi.python.org/packages/1a/2b/322d6e01ba19c1e28349efe46dab1bd480c81a55af0658d63dc48ed62ee6/WebOb-%{version}.tar.gz
%define sha1    WebOb=6f23a2eec1510ceee66efd51d3a2b7025c4cdc2b

BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python-pytest
BuildRequires:  python3-pytest
%endif

Requires:       python2
Requires:       python2-libs

%description
WebOb provides objects for HTTP requests and responses. Specifically it does this by wrapping the WSGI request environment and response status/headers/app_iter(body).

The request and response objects provide many conveniences for parsing HTTP request and forming HTTP responses. Both objects are read/write: as a result, WebOb is also a nice way to create HTTP requests and parse HTTP responses.

%package -n     python3-webob
Summary:        python-webob
Requires:       python3
Requires:       python3-libs

%description -n python3-webob
Python 3 version.

%prep
%setup -q -n WebOb-%{version}
%{__rm} -f tests/performance_test.py
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-webob
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.8.2-1
-   Update to version 1.8.2
*   Mon Aug 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.2-3
-   Fixed make check errors
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.2-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Mar 30 2017 Siju Maliakkal <smaliakkal@vmware.com> 1.7.2-1
-   Updating package to 1.7.2-1
*   Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.1-1
-   Initial packaging for Photon
