%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Coroutine-based network library
Name:           python-gevent
Version:        1.2.1
Release:        3%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/gevent
Source0:        gevent-%{version}.tar.gz
%define sha1    gevent=30bb949c572a637341db4fe52e575d44cef937b3

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python2-devel

Requires:       python2
Requires:       python2-libs
Requires:       python-greenlet

%description
gevent is a coroutine-based Python networking library.
Features include:
    Fast event loop based on libev.
    Lightweight execution units based on greenlet.
    Familiar API that re-uses concepts from the Python standard library.
    Cooperative sockets with SSL support.
    DNS queries performed through c-ares or a threadpool.
    Ability to use standard library and 3rd party modules written for standard blocking sockets

%package -n     python3-gevent
Summary:        python-gevent
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs
Requires:       python3-greenlet

%description -n python3-gevent
Python 3 version.

%prep
%setup -q -n gevent-%{version}

%build
python2 setup.py build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install py
python2 setup.py test
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-gevent
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.2.1-3
-   Removed erroneous line
*   Tue May 16 2017 Rongrong Qiu <rqiu@vmware.com> 1.2.1-2
-   Add requires python-greenlet and python3-greenlet
*   Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.1-1
-   Initial packaging for Photon
