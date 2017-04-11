Summary:    low-level library for netfilter related kernel/userspace communication.
Name:       libnfnetlink
Version:    1.0.1
Release:    1%{?dist}
License:    LGPLv2.1+
URL:        http://netfilter.org/projects/libnfnetlink/
Group:      System Environment/libraries
Vendor:     VMware, Inc.
Distribution: Photon http://netfilter.org/projects/libnfnetlink/files/libnfnetlink-1.0.1.tar.bz2
Source0:     http://netfilter.org/projects/libnfnetlink/files/%{name}-%{version}.tar.bz2
%define sha1 libnfnetlink=27ae2dfbd976e28cb7a417f9e946c901f512dd9a
%description
libnfnetlink is the low-level library for netfilter related kernel/userspace communication. It provides a generic messaging infrastructure for in-kernel netfilter subsystems

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
%description devel
Libraries and header files for libnfnetlink library.

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --enable-static=no
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete

%check
make %{?_smp_mflags} -k check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/libnfnetlink.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libnfnetlink.so
%{_libdir}/pkgconfig/libnfnetlink.pc

%changelog
*   Thu Apr 06 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.0.1-1
-   Initial build.	First version
