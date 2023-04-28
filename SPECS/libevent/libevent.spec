Summary:        An Event notification library.
Name:           libevent
Version:        2.1.12
Release:        1%{?dist}
License:        BSD
URL:            http://libevent.org
Source0:        https://github.com/%{name}/%{name}/releases/download/release-%{version}-stable/%{name}-%{version}-stable.tar.gz
%define sha512  libevent=88d8944cd75cbe78bc4e56a6741ca67c017a3686d5349100f1c74f8a68ac0b6410ce64dff160be4a4ba0696ee29540dfed59aaf3c9a02f0c164b00307fcfe84f
Group:          System/Library
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  pkg-config
BuildRequires:  openssl-devel >= 1.1.1
Requires:       openssl >= 1.1.1

%description
The libevent API provides a mechanism to execute a callback function when a specific event
occurs on a file descriptor or after a timeout has been reached. Furthermore, libevent also
support callbacks due to signals or regular timeouts.

%package        devel
Summary:        Development files for libevent
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The subpackage includes all development related headers and library.

%prep
%autosetup -n %{name}-%{version}-stable

%build
%configure --disable-static --disable-libevent-regress
make %{?_smp_mflags}

%install
%makeinstall
find %{buildroot} -name '*.la' -delete

%check
make %{?_smp_mflags} -k check

%post -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_bindir}/event_rpcgen.py
%{_libdir}/*.so
%{_libdir}/pkgconfig/libevent.pc
%{_libdir}/pkgconfig/libevent_pthreads.pc
%{_libdir}/pkgconfig/libevent_openssl.pc
%{_libdir}/pkgconfig/libevent_core.pc
%{_libdir}/pkgconfig/libevent_extra.pc

%changelog
* Wed Apr 12 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.1.12-1
- Upgraded to version 2.1.12
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.1.8-3
- Bump up release for openssl
* Thu Sep 10 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.1.8-2
- Openssl 1.1.1 compatibility
* Mon Apr 03 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.1.8-1
- Upgraded to version 2.1.8. (fixes CVE-2016-10195)
* Tue Jul 26 2016 Divya Thaluru <dthaluru@vmware.com> 2.0.22-4
- Removed packaging of debug files
* Wed Jul 13 2016 Alexey Makhalov <amakhalov@vmware.com> 2.0.22-3
- Added openssl runtime requirement
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.22-2
- GA - Bump release of all rpms
*       Thu Apr 28 2016 Kumar Kaushik <kaushikk@vmware.com> 2.0.22-1
-       Initial Version.
