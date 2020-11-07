%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        XML and HTML with Python
Name:           python3-lxml
Version:        4.6.1
Release:        1%{?dist}
Group:          Development/Libraries
License:        BSD
URL:            http://lxml.de
Source0:        https://pypi.python.org/packages/39/e8/a8e0b1fa65dd021d48fe21464f71783655f39a41f218293c1c590d54eb82/lxml-%{version}.tar.gz
%define sha1    lxml=0b46582a2da69151b9b792d118df7f44670b93ca
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  libxslt
BuildRequires:  libxslt-devel
BuildRequires:  cython3
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs
Requires:       libxslt

%description
The lxml XML toolkit is a Pythonic binding for the C libraries libxml2 and libxslt. It is unique in that it combines the speed and XML feature completeness of these libraries with the simplicity of a native Python API, mostly compatible but superior to the well-known ElementTree API.


%prep
%setup -q -n lxml-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
export LC_ALL=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
make test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 4.6.1-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 4.5.2-1
-   Automatic Version Bump
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 4.2.4-3
-   Mass removal python2
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
