%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python2_version: %define python2_version %(python2 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}

Summary:        A modern, feature-rich and highly-tunable Python client library for Apache Cassandra (2.1+)
Name:           python-cassandra-driver
Version:        3.15.1
Release:        2%{?dist}
Url:            https://github.com/datastax/python-driver#datastax-python-driver-for-apache-cassandra
License:        Apache 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/datastax/python-driver/archive/cassandra-driver-%{version}.tar.gz
%define sha1    cassandra-driver=cf83c56599ef95c23c1f1b26e9d7209f2fe3ae87
BuildRequires:  python2
BuildRequires:  cython
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pip
BuildRequires:  python-pytest
BuildRequires:  libev-devel
BuildRequires:  libev
%if %{with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  iana-etc
%endif
Requires:       python2
Requires:       python2-libs

%description
A modern, feature-rich and highly-tunable Python client library for Apache Cassandra (2.1+) using exclusively Cassandra's binary protocol and Cassandra Query Language v3.
The driver supports Python 2.7, 3.3, 3.4, 3.5, and 3.6.

%package -n     python3-cassandra-driver
Summary:        python3-cassandra-driver
BuildRequires:  python3
BuildRequires:  cython3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-cassandra-driver
Python 3 version.

%prep
%setup -q -n cassandra-driver-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build --no-cython
pushd ../p3dir
python3 setup.py build --no-cython
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot} --no-cython
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --no-cython
popd

%check
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 nose
$easy_install_2 scales
$easy_install_2 mock
$easy_install_2 ccm
$easy_install_2 unittest2
$easy_install_2 pytz
$easy_install_2 sure
$easy_install_2 pure-sasl
$easy_install_2 twisted
$easy_install_2 gevent
$easy_install_2 eventlet
$easy_install_2 packaging
$easy_install_2 Netbase
python2 setup.py gevent_nosetests
python2 setup.py eventlet_nosetests
pushd ../p3dir
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 nose
$easy_install_3 scales
$easy_install_3 mock
$easy_install_3 ccm
$easy_install_3 unittest2
$easy_install_3 pytz
$easy_install_3 sure
$easy_install_3 pure-sasl
$easy_install_3 twisted
$easy_install_3 gevent
$easy_install_3 eventlet
$easy_install_3 packaging
$easy_install_3 Netbase
python3 setup.py gevent_nosetests
python3 setup.py eventlet_nosetests
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-cassandra-driver
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Dec 12 2018 Tapas Kundu <tkundu@vmware.com> 3.15.1-2
-   Fix make check
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.15.1-1
-   Update to version 3.15.1
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 3.10.0-5
-   Remove BuildArch
*   Tue Sep 12 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.10.0-4
-   Do make check for python3 subpackage
*   Wed Aug 16 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10.0-3
-   Fix make check.
*   Tue Jun 20 2017 Xiaolin Li <xiaolinl@vmware.com> 3.10.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 15 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10.0-1
-   Initial packaging for Photon
