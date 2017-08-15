Summary:        library for fast, message-based applications
Name:           zeromq
Version:        4.1.4
Release:        2%{?dist}
URL:            http://www.zeromq.org
License:        LGPLv3+
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://archive.org/download/zeromq_4.1.4/%{name}-%{version}.tar.gz
%define sha1 zeromq=b632a4b6f8a14390dc17824e37ff7b10831ce2b4
Requires:       libstdc++

%description
The 0MQ lightweight messaging kernel is a library which extends the standard
socket interfaces with features traditionally provided by specialised messaging
middleware products. 0MQ sockets provide an abstraction of asynchronous message
queues, multiple messaging patterns, message filtering (subscriptions), seamless
access to multiple transport protocols and more.

%package    devel
Summary:    Header and development files for zeromq
Requires:   %{name} = %{version}
%description    devel
It contains the libraries and header files to create applications 

%prep
%setup -q
%build
./configure \
    --prefix=%{_prefix} \
    --with-libsodium=no \
    --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete

%check
mount -t devpts -o gid=4,mode=620 none /dev/pts
ulimit -n 1200 && make check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING COPYING.LESSER NEWS
%{_bindir}/
%{_libdir}/libzmq.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libzmq.so
%{_libdir}/pkgconfig/libzmq.pc
%{_includedir}/
%{_mandir}/*

%changelog
*   Mon Aug 07 2017 Chang Lee <changlee@vmware.com> 4.1.4-2
-   Fixed %check
*   Thu Apr 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.1.4-1
-   Initial build. First version
