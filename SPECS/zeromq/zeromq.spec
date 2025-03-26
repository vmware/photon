Summary:        library for fast, message-based applications
Name:           zeromq
Version:        4.3.4
Release:        3%{?dist}
URL:            http://www.zeromq.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/zeromq/libzmq/releases/download/v%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Requires:       libstdc++

%description
The 0MQ lightweight messaging kernel is a library which extends the standard
socket interfaces with features traditionally provided by specialised messaging
middleware products. 0MQ sockets provide an abstraction of asynchronous message
queues, multiple messaging patterns, message filtering (subscriptions), seamless
access to multiple transport protocols and more.

%package        devel
Summary:        Header and development files for zeromq
Requires:       %{name} = %{version}
%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%configure \
    --with-libsodium=no \
    --disable-Werror \
    --disable-static
%make_build

%install
%make_install
find %{buildroot}%{_libdir} -name '*.la' -delete

%check
make check %{_smp_mflags}

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
*   Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 4.3.4-3
-   Release bump for SRP compliance
*   Fri Aug 19 2022 Ajay Kaher <akaher@vmware.com> 4.3.4-2
-   fix: build fails with gcc 12
*   Fri Jul 09 2021 Nitesh Kumar <kunitesh@vmware.com> 4.3.4-1
-   Upgrade to 4.3.4
*   Thu Sep 10 2020 Gerrit Photon <photon-checkins@vmware.com> 4.3.3-1
-   Automatic Version Bump
*   Thu Jun 25 2020 Gerrit Photon <photon-checkins@vmware.com> 4.3.2-1
-   Automatic Version Bump
*   Mon Jul 22 2019 Siju Maliakkal <smaliakkal@vmware.com> 4.2.3-2
-   Apply patch for CVE-2019-13132
*   Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 4.2.3-1
-   Updated to latest version
*   Fri Sep 15 2017 Bo Gan <ganb@vmware.com> 4.1.4-3
-   Remove devpts mount
*   Mon Aug 07 2017 Chang Lee <changlee@vmware.com> 4.1.4-2
-   Fixed %check
*   Thu Apr 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.1.4-1
-   Initial build. First version
