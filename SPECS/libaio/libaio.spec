Summary:        Linux-native asynchronous I/O access library
Name:           libaio
Version:        0.3.113
Release:        1%{?dist}
URL:            https://github.com/yugabyte/libaio
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://releases.pagure.org/libaio/libaio-0.3.113.tar.gz

Source1: license.txt
%include %{SOURCE1}

%if 0%{?with_check}
BuildRequires:  e2fsprogs
BuildRequires:  e2fsprogs-libs
%endif

%description
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has a
richer API and capability set than the simple POSIX async I/O facility.
This library, libaio, provides the Linux-native API for async I/O.
The POSIX async I/O facility requires this library in order to provide
kernel-accelerated async I/O capabilities, as do applications which
require the Linux-native async I/O API.

%package        devel
Summary:        Development files for Linux-native asynchronous I/O access
Group:          Development/System
Requires:       libaio

%description    devel
This package provides header files to include and libraries to link with
for the Linux-native asynchronous I/O facility ("async I/O", or "aio").

%prep
# Using autosetup is not feasible
%setup -q -a 0

%build
cd %{name}-%{version}
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} prefix=%{_usr} libdir=%{_libdir} %{?_smp_mflags}

%check
make %{?_smp_mflags} -k check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%attr(0755,root,root) %{_libdir}/libaio.so.*
%doc COPYING TODO

%files devel
%attr(0644,root,root) %{_includedir}/*
%attr(0755,root,root) %{_libdir}/libaio.so
%exclude %attr(0755,root,root) %{_libdir}/libaio.a

%changelog
* Mon Apr 28 2025 Tapas Kundu <tapas.kundu@broadcom.com> 0.3.113-1
- Update to 0.3.113
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.3.110-4
- Release bump for SRP compliance
* Mon Aug 19 2019 Shreenidhi Shedi <sshedi@vmware.com> 0.3.110-3
- Fix make check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.3.110-2
- GA - Bump release of all rpms
* Tue Mar 3 2015 Divya Thaluru <dthaluru@vmware.com> 0.3.110-1
- Initial version
