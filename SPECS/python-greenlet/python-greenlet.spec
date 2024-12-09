Summary:        Lightweight in-process concurrent programming
Name:           python3-greenlet
Version:        2.0.0
Release:        2%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.python.org/pypi/greenlet
Source0:        greenlet-%{version}.tar.gz
%define sha512  greenlet=2c4ae0623e8258a85012fca3c4c419cab3634679dc05a51b9079bcae3afb6f6c3c5052b249dbdb48a8dac3d20b9313343b217862ab34f3ae6dd5cda66e53dc35

Source1: license.txt
%include %{SOURCE1}

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
%autosetup -n greenlet-%{version}

%build
%py3_build

%install
%py3_install

%check
#make check test code only support python2
#python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
/usr/include/python%{python3_version}/greenlet/greenlet.h

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.0.0-2
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.0.0-1
- Update to 2.0.0
* Tue Oct 13 2020 Tapas Kundu <tkundu@vmware.com> 0.4.17-2
- Use python3.9
* Tue Sep 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.4.17-1
- Automatic Version Bump
* Sun Jul 26 2020 Tapas Kundu <tkundu@vmware.com> 0.4.16-2
- Use python3.8
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.4.16-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.4.15-3
- Mass removal python2
* Fri Oct 05 2018 Tapas Kundu <tkundu@vmware.com> 0.4.15-2
- Updated using python 3.7
- removed buildrequires from subpackages
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.4.15-1
- Update to version 0.4.15
* Fri Aug 11 2017 Rongrong Qiu <rqiu@vmware.com> 0.4.12-3
- make check only support python3 for bug 1937030
* Thu Apr 27 2017 Siju Maliakkal <smaliakkal@vmware.com> 0.4.12-2
- updated python version
* Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 0.4.12-1
- Initial packaging for Photon
