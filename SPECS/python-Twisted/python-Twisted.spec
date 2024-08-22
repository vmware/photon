%global debug_package   %{nil}
%define srcname Twisted

Summary:        An asynchronous networking framework written in Python
Name:           python3-Twisted
Version:        22.10.0
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://twistedmatrix.com

Source0: https://pypi.python.org/packages/source/T/Twisted/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=36adac424f6776c7db870d2291713da41054e974dfac0dbc1cbd55f76915a92073bcb25d4593b82e229d154d5297c67e7ba82d808921d206c97c8024bd5431a8

Patch0: no_packet.patch
Patch1: 0001-sslverify.py-use-fips-compatible-sha512-instead-of-m.patch

BuildRequires: python3-devel
BuildRequires: python3-incremental
BuildRequires: python3-zope.interface
BuildRequires: python3-setuptools
BuildRequires: python3-xml
BuildRequires: python3-automat

%if 0%{?with_check}
BuildRequires: net-tools
BuildRequires: sudo
BuildRequires: shadow
BuildRequires: curl-devel
BuildRequires: python3-pip
BuildRequires: python3-constantly
%endif

Requires: python3
Requires: python3-zope.interface
Requires: python3-netaddr
Requires: python3-incremental
Requires: python3-constantly
Requires: python3-hyperlink
Requires: python3-attrs
Requires: python3-PyHamcrest
Requires: python3-service_identity >= 18.1.0
Requires: python3-typing-extensions

%description
Twisted is a networking engine written in Python, supporting numerous protocols.
It contains a web server, numerous chat clients, chat servers, mail servers and more.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}

for fn in twistd trial tkconch pyhtmlizer twist conch ckeygen cftp; do
  ln -sv ${fn} %{buildroot}%{_bindir}/${fn}3
done

%if 0%{?with_check}
%check
export LC_ALL=C
PATH=%{buildroot}%{_bindir}:$PATH \
     PYTHONPATH=%{buildroot}%{python3_sitelib} \
     %{buildroot}%{_bindir}/trial twisted
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/mailmail
%{_bindir}/twistd*
%{_bindir}/trial*
%{_bindir}/tkconch*
%{_bindir}/pyhtmlizer*
%{_bindir}/twist*
%{_bindir}/conch*
%{_bindir}/ckeygen*
%{_bindir}/cftp*

%changelog
* Thu Aug 22 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 22.10.0-1
- Update to 22.10.0, Fixes multiple CVEs
* Wed May 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 20.3.0-4
- Use fips allowed hashing algorithms in sslverify
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 20.3.0-3
- Bump up to compile with python 3.10
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 20.3.0-2
- Fix build with new rpm
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 20.3.0-1
- Automatic Version Bump
* Wed Jul 08 2020 Tapas Kundu <tkundu@vmware.com> 19.10.0-5
- Mass removal python2
* Sat Jun 27 2020 Tapas Kundu <tkundu@vmware.com> 19.10.0-4
- Address CVE-2020-10108 and CVE-2020-10109
* Mon Jun 01 2020 Tapas Kundu <tkundu@vmware.com> 19.10.0-3
- Requires service_identity
* Wed Mar 04 2020 Tapas Kundu <tkundu@vmware.com> 19.10.0-2
- Fix make check
* Mon Nov 18 2019 Tapas Kundu <tkundu@vmware.com> 19.10.0-1
- Updated to 19.10.0 release
* Fri Aug 30 2019 Tapas Kundu <tkundu@vmware.com> 18.7.0-3
- Added requires as PyHamcrest
* Tue Oct 30 2018 Tapas Kundu <tkundu@vmware.com> 18.7.0-2
- Moved build requires from subpackage
- Added attrs package in requires.
* Thu Sep 13 2018 Tapas Kundu <tkundu@vmware.com> 18.7.0-1
- Upgraded to release 18.7.0
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 17.5.0-3
- Remove BuildArch
* Mon Sep 11 2017 Dheeraj Shetty <dheerajs@vmware.com> 17.5.0-2
- Added python-automat, python-hyperlink and its python3 version to the
- requires.
* Tue Aug 29 2017 Dheeraj Shetty <dheerajs@vmware.com> 17.5.0-1
- Upgrade version
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 17.1.0-6
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 17.1.0-5
- Adding python3 scripts to bin directory
* Tue May 09 2017 Rongrong Qiu <rqiu@vmware.com> 17.1.0-4
- Added python-constantly to the requires.
* Mon Mar 27 2017 Xiaolin Li <xiaolinl@vmware.com> 17.1.0-3
- Added python-netaddr and python-incremental to the requires.
* Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> 17.1.0-2
- Change requires
* Wed Mar 01 2017 Xiaolin Li <xiaolinl@vmware.com> 17.1.0-1
- Added python3 package and updated to version 17.1.0.
* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 15.5.0-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 15.5.0-2
- GA - Bump release of all rpms
* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 15.5.0-1
- Upgrade version
* Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
