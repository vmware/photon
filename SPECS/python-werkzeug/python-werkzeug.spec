%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        The Swiss Army knife of Python web development
Name:           python3-werkzeug
Version:        1.0.1
Release:        2%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/Werkzeug
Source0:        https://pypi.python.org/packages/ab/65/d3f1edd1109cb1beb6b82f4139addad482df5b5ea113bdc98242383bf402/Werkzeug-%{version}.tar.gz
%define sha1    Werkzeug=07b0f2dcd460076d437d1481c556584db88df199

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python3-requests
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif
Requires:       python3
Requires:       python3-libs
BuildArch:      noarch

%description
Werkzeug started as simple collection of various utilities for WSGI applications and has become one of the most advanced WSGI utility modules. It includes a powerful debugger, full featured request and response objects, HTTP utilities to handle entity tags, cache control headers, HTTP dates, cookie handling, file uploads, a powerful URL routing system and a bunch of community contributed addon modules.

%prep
%setup -q -n Werkzeug-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 23)
$easy_install_3 pytest hypothesis
LANG=en_US.UTF-8 PYTHONPATH=./  python3 setup.py test

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.0.1-2
-   openssl 1.1.1
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.1-1
-   Automatic Version Bump
*   Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 0.14.1-3
-   Mass removal python2
*   Mon Dec 03 2018 Tapas Kundu <tkundu@vmware.com> 0.14.1-2
-   Fix make check
-   Moved buildrequires from subpackage
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.14.1-1
-   Update to version 0.14.1
*   Tue Jul 25 2017 Divya Thaluru <dthaluru@vmware.com> 0.12.1-2
-   Fixed rpm check errors
*   Thu Mar 30 2017 Siju Maliakkal <smaliakkal@vmware.com> 0.12.1-1
-   Updating package to latest
*   Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 0.11.15-1
-   Initial packaging for Photon.
