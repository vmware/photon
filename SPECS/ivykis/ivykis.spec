Summary:    libivykis async I/O-assisting library
Name:       ivykis
Version:    0.42.4
Release:    2%{?dist}
URL:        http://libivykis.sourceforge.net
Group:      System Environment/Development
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    http://downloads.sourceforge.net/project/libivykis/%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  gcc

%description
ivykis is a library for asynchronous I/O readiness notification.
It is a thin, portable wrapper around OS-provided mechanisms such
as epoll_create(2), kqueue(2), poll(2), poll(7d) (/dev/poll) and
port_create(3C).

%package  devel
Summary:  Header and development files
Requires: %{name} = %{version}-%{release}

%description  devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot}%{_libdir} -name '*.la' -delete

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING
%{_libdir}/libivykis.so.*

%files devel
%defattr(-,root,root)
%{_includedir}
%{_mandir}/man3/*.3*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*   Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 0.42.4-2
-   Release bump for SRP compliance
*   Thu Aug 06 2020 Ankit Jain <ankitja@vmware.com> 0.42.4-1
-   Initial build.  First version
