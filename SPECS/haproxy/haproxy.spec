Summary:        A fast, reliable HA, load balancing, and proxy solution.
Name:           haproxy
Version:        2.5.5
Release:        1%{?dist}
License:        GPL
URL:            http://www.haproxy.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.haproxy.org/download/2.0/src/%{name}-%{version}.tar.gz
%define sha1    haproxy=a5fb147507f8c1f08b2aded0dc9c16baf1b5dc69

BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  lua-devel
BuildRequires:  pkg-config
BuildRequires:  zlib-devel
BuildRequires:  systemd-devel
Requires:       systemd

%description
HAProxy is a fast and reliable solution offering high availability, load
balancing, and proxying for TCP and HTTP-based applications. It is suitable
for very high traffic web-sites.

%package        doc
Summary:        Documentation for haproxy
Requires:       %{name} = %{version}-%{release}

%description    doc
It contains the documentation and manpages for haproxy package.

%prep
%autosetup -p1

%build
make %{?_smp_mflags} TARGET=linux-glibc USE_PCRE=1 USE_OPENSSL=1 \
        USE_GETADDRINFO=1 USE_ZLIB=1 USE_SYSTEMD=1
make %{?_smp_mflags} -C admin/systemd
sed -i s/"local\/"/""/g admin/systemd/haproxy.service
sed -i "s/\/run/\/var\/run/g" admin/systemd/haproxy.service
sed -i "s/192.168.1.22/127.0.0.0/g" examples/transparent_proxy.cfg

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} PREFIX=%{_prefix} DOCDIR=%{_docdir}/haproxy TARGET=linux-glibc install %{?_smp_mflags}
install -vDm755 admin/systemd/haproxy.service \
       %{buildroot}/usr/lib/systemd/system/haproxy.service
install -vDm644 examples/transparent_proxy.cfg  %{buildroot}/%{_sysconfdir}/haproxy/haproxy.cfg

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/systemd/system/haproxy.service
%{_sysconfdir}/haproxy/haproxy.cfg

%files doc
%defattr(-,root,root,-)
%{_docdir}/haproxy/*
%{_mandir}/*

%changelog
*   Tue Mar 15 2022 Nitesh Kumar <kunitesh@vmware.com> 2.5.5-1
-   Upgrade to 2.5.5, Address CVE-2022-0711
*   Wed Nov 10 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.3.10-3
-   openssl 3.0.0
*   Fri Sep 17 2021 Nitesh Kumar <kunitesh@vmware.com> 2.3.10-2
-   Fix CVE-2021-40346
*   Thu May 06 2021 Gerrit Photon <photon-checkins@vmware.com> 2.3.10-1
-   Automatic Version Bump
*   Fri Feb 05 2021 Susant Sahani <ssahani@vmware.com> 2.3.4-1
-   Version bump
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.2.2-2
-   openssl 1.1.1
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.2.2-1
-   Automatic Version Bump
*   Thu Mar 05 2020 Ashwin H <ashwinh@vmware.com> 2.0.10-1
-   Update to version 2.0.10 to fix CVE-2019-19330
*   Thu Nov 7 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.0.6-1
-   Update to 2.0.6
*   Tue Apr 2 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-1
-   Update to 1.9.6
*   Thu Feb 28 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.14-2
-   Patch for CVE_2018_20102
-   Patch for CVE_2018_20103
*   Tue Dec 04 2018 Ajay Kaher <akaher@vmware.com> 1.8.14-1
-   Update to version 1.8.14
*   Thu Oct 25 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 1.8.13-2
-   Build with USE_SYSTEMD=1 to fix service startup.
*   Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 1.8.13-1
-   Update to version 1.8.13
*   Tue Apr 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.6.12-1
-   Updated to version 1.6.12
*   Sun Nov 27 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.6.10-1
-   Upgrade to 1.6.10 to address CVE-2016-5360
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.3-3
-   GA - Bump release of all rpms
*   Fri May 20 2016 Xiaolin Li <xiaolinl@vmware.com> 1.6.3-2
-   Add haproxy-systemd-wrapper to package, add a default configuration file.
*   Mon Feb 22 2016 Xiaolin Li <xiaolinl@vmware.com> 1.6.3-1
-   Updated to version 1.6.3
*   Thu Oct 01 2015 Vinay Kulkarni <kulkarniv@vmware.com> 1.5.14-1
-   Add haproxy v1.5 package.
