%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        The Swiss Army knife of Python web development
Name:           python-werkzeug
Version:        0.14.1
Release:        2%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/Werkzeug
Source0:        https://pypi.python.org/packages/ab/65/d3f1edd1109cb1beb6b82f4139addad482df5b5ea113bdc98242383bf402/Werkzeug-%{version}.tar.gz
%define sha1    Werkzeug=4b979fb960c5b5507ccb8a705931fa217013483d

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-incremental
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python-requests
BuildRequires:  python3-requests
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif
Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
Werkzeug started as simple collection of various utilities for WSGI applications and has become one of the most advanced WSGI utility modules. It includes a powerful debugger, full featured request and response objects, HTTP utilities to handle entity tags, cache control headers, HTTP dates, cookie handling, file uploads, a powerful URL routing system and a bunch of community contributed addon modules.

%package -n     python3-werkzeug
Summary:        python-werkzeug
Requires:       python3
Requires:       python3-libs
%description -n python3-werkzeug
Python 3 version.

%prep
%setup -q -n Werkzeug-%{version}

%build
python2 setup.py build
python3 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 pytest hypothesis
LANG=en_US.UTF-8 PYTHONPATH=./  python2 setup.py test

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-werkzeug
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
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
