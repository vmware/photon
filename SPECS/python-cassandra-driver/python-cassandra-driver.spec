%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}

Summary:        A modern, feature-rich and highly-tunable Python client library for Apache Cassandra (2.1+)
Name:           python3-cassandra-driver
Version:        3.24.0
Release:        3%{?dist}
Url:            https://github.com/datastax/python-driver#datastax-python-driver-for-apache-cassandra
License:        Apache 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/datastax/python-driver/archive/cassandra-driver-%{version}.tar.gz
%define sha1    cassandra-driver=3affe07f7c0bea76d202f60627d11c3b445908c0

BuildRequires:  python3
BuildRequires:  cython3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  libev-devel
BuildRequires:  libev

%if %{with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-packaging
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  iana-etc
%endif

Requires:       python3
Requires:       python3-libs

%description
A modern, feature-rich and highly-tunable Python client library for Apache Cassandra (2.1+)
using exclusively Cassandra's binary protocol and Cassandra Query Language v3. The driver
supports Python 2.7, 3.3, 3.4, 3.5, and 3.6.

%prep
%setup -q -n cassandra-driver-%{version}

%build
python3 setup.py build --no-cython

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --no-cython

%check
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

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 3.24.0-3
-   Fix build with new rpm
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.24.0-2
-   openssl 1.1.1
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.24.0-1
-   Automatic Version Bump
*   Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 3.15.1-3
-   Mass removal python2
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
