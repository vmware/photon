%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-ndg-httpsclient
Version:        0.5.1
Release:        2%{?dist}
Summary:        Enhanced HTTPS support for httplib and urllib2 using PyOpenSSL.
License:        BSD
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/ndg-httpsclient
Source0:        ndg_httpsclient-%{version}.tar.gz
%define sha1    ndg_httpsclient=aa0b3c2d8ada61fa3f4e82ed307056b14cc63cb9
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-pip
BuildRequires:  python-setuptools
%if %{with_check}
BuildRequires:  python-urllib3
BuildRequires:  python-pyOpenSSL
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  libffi-devel
%endif
Requires:       python2
Requires:       python2-libs
Requires:       python-setuptools
BuildArch:      noarch

%description
Enhanced HTTPS support for httplib and urllib2 using PyOpenSSL.

%package -n     python3-ndg-httpsclient
Summary:        Python3 version of ndg-httpsclient.
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-urllib3
BuildRequires:  python3-pyOpenSSL
%endif

%description -n python3-ndg-httpsclient
Python3 version of ndg-httpsclient.

%prep
%setup -n ndg_httpsclient-%{version}
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

%check
pushd ndg/httpsclient/test

openssl s_server -www -cert pki/localhost.crt -key pki/localhost.key -accept 4443 &
openssl_pid=$!

PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python2_sitelib} \
python2 test_urllib2.py
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python2_sitelib} \
python2 test_https.py
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python2_sitelib} \
python2 test_utils.py

PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
python3 test_urllib2.py
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
python3 test_https.py
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
python3 test_utils.py

kill $openssl_pid

popd

%files
%defattr(-,root,root,-)
%{_bindir}/ndg_httpclient
%{python2_sitelib}/*

%files -n python3-ndg-httpsclient
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Dec 05 2018 Ashwin H <tkundu@vmware.com> 0.5.1-2
-   Add %check
*   Sat Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.5.1-1
-   Updated to 0.5.1
*   Tue Aug 29 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.4.2-1
-   Initial version of python ndg-httpsclient for PhotonOS.
