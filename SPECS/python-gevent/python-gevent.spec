%define srcname gevent

Summary:        Coroutine-based network library
Name:           python3-gevent
Version:        21.8.0
Release:        3%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/gevent

Source0: gevent-%{version}.tar.gz
%define sha512 %{srcname}=dae95f986530e79b07a0006f6fb4cbd3911ac0bf2e58c4896ee5fa6d2e2a9ed5785c346958ee23cd57c2dcafb0a34c585b1f6375a29fd653e061a382482fc9fb

Patch0: CVE-2023-41419.patch

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-xml
BuildRequires: python3-zope.interface

%if 0%{?with_check}
BuildRequires: lsof
BuildRequires: curl-devel
BuildRequires: openssl-devel
BuildRequires: python3-test
BuildRequires: python3-pip
%endif

Requires: python3
Requires: python3-greenlet
Requires: python3-zope.event
Requires: python3-zope.interface

%description
gevent is a coroutine-based Python networking library.
Features include:
- Fast event loop based on libev.
- Lightweight execution units based on greenlet.
- Familiar API that re-uses concepts from the Python standard library.
- Cooperative sockets with SSL support.
- DNS queries performed through c-ares or a threadpool.
- Ability to use standard library and 3rd party modules written for standard blocking sockets

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install nose
python3 setup.py develop
nosetests

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Mon Dec 16 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 21.8.0-3
- Fix CVE-2023-41419
* Thu Aug 10 2023 Shreenidhi Shedi <sshedi@vmware.com> 21.8.0-2
- Add zope.interface to requires
* Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 21.8.0-1
- Update release to compile with python 3.10
* Tue Feb 23 2021 Tapas Kundu <tkundu@vmware.com> 20.9.0-3
- Added requires for python3-zope.event
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 20.9.0-2
- openssl 1.1.1
* Tue Sep 22 2020 Gerrit Photon <photon-checkins@vmware.com> 20.9.0-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 20.6.2-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 1.3.6-3
- Mass removal python2
* Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> 1.3.6-2
- Fix make check
* Wed Sep 12 2018 Tapas Kundu <tkundu@vmware.com> 1.3.6-1
- Updated to version 1.3.6
* Wed Sep 20 2017 Bo Gan <ganb@vmware.com> 1.2.1-6
- Fix build and make check issues
* Wed Sep 13 2017 Rongrong Qiu <rqiu@vmware.com> 1.2.1-5
- Update make check for bug 1900401
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.1-4
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.2.1-3
- Removed erroneous line
* Tue May 16 2017 Rongrong Qiu <rqiu@vmware.com> 1.2.1-2
- Add requires python-greenlet and python3-greenlet
* Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.1-1
- Initial packaging for Photon
