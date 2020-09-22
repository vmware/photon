%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Lightweight in-process concurrent programming
Name:           python3-greenlet
Version:        0.4.17
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.python.org/pypi/greenlet
Source0:        greenlet-%{version}.tar.gz
%define sha1    greenlet=59d0c79e82ac60c3fe00179d355e34493aebae27

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel

Requires:       python3
Requires:       python3-libs

%description
The greenlet package is a spin-off of Stackless, a version of CPython that supports micro-threads called “tasklets”. Tasklets run pseudo-concurrently (typically in a single or a few OS-level threads) and are synchronized with data exchanges on “channels”.

A “greenlet”, on the other hand, is a still more primitive notion of micro-thread with no implicit scheduling; coroutines, in other words. This is useful when you want to control exactly when your code runs. You can build custom scheduled micro-threads on top of greenlet; however, it seems that greenlets are useful on their own as a way to make advanced control flow structures. For example, we can recreate generators; the difference with Python’s own generators is that our generators can call nested functions and the nested functions can yield values too. Additionally, you don’t need a “yield” keyword. See the example in tests/test_generator.py.


%prep
%setup -q -n greenlet-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
#make check test code only support python2
#python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
/usr/include/python3.8/greenlet/greenlet.h

%changelog
*   Tue Sep 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.4.17-1
-   Automatic Version Bump
*   Sun Jul 26 2020 Tapas Kundu <tkundu@vmware.com> 0.4.16-2
-   Use python3.8
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.4.16-1
-   Automatic Version Bump
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.4.15-3
-   Mass removal python2
*   Fri Oct 05 2018 Tapas Kundu <tkundu@vmware.com> 0.4.15-2
-   Updated using python 3.7
-   removed buildrequires from subpackages
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.4.15-1
-   Update to version 0.4.15
*   Fri Aug 11 2017 Rongrong Qiu <rqiu@vmware.com> 0.4.12-3
-   make check only support python3 for bug 1937030
*   Thu Apr 27 2017 Siju Maliakkal <smaliakkal@vmware.com> 0.4.12-2
-   updated python version
*   Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 0.4.12-1
-   Initial packaging for Photon
