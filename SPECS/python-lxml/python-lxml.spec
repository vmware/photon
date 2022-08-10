%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        XML and HTML with Python
Name:           python-lxml
Version:        4.9.1
Release:        1%{?dist}
Group:          Development/Libraries
License:        BSD
URL:            http://lxml.de
Source0:        https://github.com/lxml/lxml/releases/download/lxml-%{version}/lxml-%{version}.tar.gz
%define sha512  lxml=d7ec55c7db2c63a716ca5f4d833706d90fc76c944885e010fcdb96786bcfe796994e438450cf4e8e6e75d702e21fb16971f28f854d7a1f76c34e4ae315414d84
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-xml
BuildRequires:  libxslt
BuildRequires:  libxslt-devel
BuildRequires:  cython
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python-setuptools
BuildRequires:  python3-setuptools
Requires:       python2
Requires:       libxslt

%description
The lxml XML toolkit is a Pythonic binding for the C libraries libxml2 and libxslt. It is unique in that it combines the speed and XML feature completeness of these libraries with the simplicity of a native Python API, mostly compatible but superior to the well-known ElementTree API.

%package -n     python3-lxml
Summary:        python-lxml
Requires:       libxslt
Requires:       python3
Requires:       python3-libs

%description -n python3-lxml
Python 3 version.

%prep
%autosetup -p1 -n lxml-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --skip-build --root %{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
export LC_ALL=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
make %{?_smp_mflags} test
pushd ../p3dir
make %{?_smp_mflags} test
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python2_sitelib}/lxml/*
%{python2_sitelib}/lxml-%{version}-py2.7.egg-info

%files -n python3-lxml
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Mon Aug 08 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.9.1-1
-   Upgrade to 4.9.1
*   Mon Jul 18 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.7.1-1
-   Upgrade to 4.7.1 and fix CVE-2022-2309
*   Sun Jun 19 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.2.5-2
-   Bump version as a part of libxslt upgrade
*   Mon Jun 13 2022 Harinadh D <hdommaraju@vmware.com> 4.2.5-1
-   fix CVE-2021-28957,CVE-2018-19787
*   Thu Feb 03 2022 Harinadh D <hdommaraju@vmware.com> 4.2.4-3
-   Fix CVE-2021-43818
*   Wed Nov 28 2018 Tapas Kundu <tkundu@vmware.com> 4.2.4-2
-   Fix make check
-   moved build requires from subpackage
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 4.2.4-1
-   Update to version 4.2.4
*   Mon Aug 07 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.7.3-3
-   set LC_ALL and LANGUAGE for the tests to pass
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.7.3-2
-   Use python2_sitelib
*   Mon Apr 03 2017 Sarah Choi <sarahc@vmware.com> 3.7.3-1
-   Update to 3.7.3
*   Wed Feb 08 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.0b1-4
-   Added python3 site-packages.
*   Tue Oct 04 2016 ChangLee <changlee@vmware.com> 3.5.0b1-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.5.0b1-2
-   GA - Bump release of all rpms
*   Wed Oct 28 2015 Divya Thaluru <dthaluru@vmware.com> 3.5.0b1-1
-   Initial build.
