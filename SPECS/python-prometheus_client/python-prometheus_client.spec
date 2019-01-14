%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-prometheus_client
Version:        0.3.1
Release:        2%{?dist}
Summary:        Python client for the Prometheus monitoring system.
License:        Apache-2.0
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/prometheus_client
Source0:        prometheus_client-%{version}.tar.gz
%define sha1    prometheus_client=43aed68fa484883fa53be38f1bf19790ea9a4438
Source1:        client_python-tests-%{version}.tar.gz
%define sha1    client_python-tests=7246482ee8008d75d63e82889d512e3c9034c192 
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python-pytest
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pytest
Requires:       python2
Requires:       python2-libs
Requires:       python-setuptools
BuildArch:      noarch

%description
Python client for the Prometheus monitoring system.

%package -n     python3-prometheus_client
Summary:        python-prometheus_client
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools

%description -n python3-prometheus_client
Python 3 version.

%prep
%setup -n prometheus_client-%{version}
tar xf %{SOURCE1} --no-same-owner
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
#test incompatible with python2
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%files -n python3-prometheus_client
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> 0.3.1-2
-   Fix make check
-   uploaded test source
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.3.1-1
-   Update to version 0.3.1
*   Tue Sep 19 2017 Bo Gan <ganb@vmware.com> 0.0.20-2
-   fix make check issue by using upstream sources
*   Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.0.20-1
-   Initial version of python-prometheus_client package for Photon.
