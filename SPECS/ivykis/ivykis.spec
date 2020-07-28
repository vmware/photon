Summary:    libivykis async I/O-assisting library
Name:       ivykis
Version:    0.42.4
Release:    1%{?dist}
License:    LGPLv2+
URL:        http://libivykis.sourceforge.net
Group:      System Environment/Development
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    http://downloads.sourceforge.net/project/libivykis/%{version}/%{name}-%{version}.tar.gz
%define sha1 ivykis=d7f0766d20a4b6ac6850a47e1ec5145ee515bd54
BuildRequires:  gcc

%description
ivykis is a library for asynchronous I/O readiness notification.
It is a thin, portable wrapper around OS-provided mechanisms such
as epoll_create(2), kqueue(2), poll(2), poll(7d) (/dev/poll) and
port_create(3C).

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}

%description	devel
It contains the libraries and header files to create applications

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
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
*   Thu Aug 06 2020 Ankit Jain <ankitja@vmware.com> 0.42.4-1
-   Initial build.  First version
