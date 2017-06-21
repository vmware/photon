%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python2_version: %define python2_version %(python2 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}

Summary:        A modern, feature-rich and highly-tunable Python client library for Apache Cassandra (2.1+)
Name:           python-cassandra-driver
Version:        3.10.0
Release:        2%{?dist}
Url:            https://github.com/datastax/python-driver#datastax-python-driver-for-apache-cassandra
License:        Apache 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/datastax/python-driver/archive/%{name}-%{version}.tar.gz
%define sha1    python-cassandra-driver=1eb85a0979b6b480b53c7a725018cc0991599a60
BuildArch:      x86_64
BuildRequires:  python2
BuildRequires:  cython
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pytest
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
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-cassandra-driver
Python 3 version.

%prep
%setup -q -n python-driver-%{version}
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
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python2_sitelib} \
    py.test-%{python2_version} -v
pushd ../p3dir
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    py.test-%{python3_version} -v
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-cassandra-driver
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Tue Jun 20 2017 Xiaolin Li <xiaolinl@vmware.com> 3.10.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 15 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10.0-1
-   Initial packaging for Photon
