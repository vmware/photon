Summary:        Linux-native asynchronous I/O access library
Name:           libaio
Version:        0.3.110
Release:        4%{?dist}
URL:            https://git.fedorahosted.org/git/libaio.git
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://fedorahosted.org/releases/l/i/libaio/libaio-0.3.110.tar.gz
%define sha512 %{name}=664295d330d6e9adc005e2331e77582619625b479ffc2b81728ba6a682487380ee936079c4a69d35144b458bbe35c612f4ed9b32e913bd7e109b824345763eb3

Source1: license.txt
%include %{SOURCE1}

Patch0:        libaio-install-to-destdir-slash-usr.patch

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
%patch0 -p0 -b .install-to-destdir-slash-usr
%patch0 -p1 -b .install-to-destdir-slash-usr

%build
# A library with a soname of 1.0.0 was inadvertantly released.  This
# build process builds a version of the library with the broken soname in
# the libaio-0.3.103 directory, and then builds the library again
# with the correct soname.
cd %{name}-%{version}
make soname='libaio.so.1.0.0' libname='libaio.so.1.0.0' %{?_smp_mflags}
cd ..
make %{?_smp_mflags}

%install
cd %{name}-%{version}
install -D -m 755 src/libaio.so.1.0.0 %{buildroot}/%{_libdir}/libaio.so.1.0.0
cd ..
make destdir=%{buildroot} prefix=%{_prefix} libdir=/lib usrlibdir=%{_libdir} includedir=%{_includedir} install %{?_smp_mflags}

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
%attr(0755,root,root) %{_libdir}/libaio.a

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.3.110-4
- Release bump for SRP compliance
* Mon Aug 19 2019 Shreenidhi Shedi <sshedi@vmware.com> 0.3.110-3
- Fix make check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.3.110-2
- GA - Bump release of all rpms
* Tue Mar 3 2015 Divya Thaluru <dthaluru@vmware.com> 0.3.110-1
- Initial version
