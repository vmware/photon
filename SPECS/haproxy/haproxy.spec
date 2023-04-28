Summary:        A fast, reliable HA, load balancing, and proxy solution.
Name:           haproxy
Version:        2.2.6
Release:        6%{?dist}
License:        GPL
URL:            http://www.haproxy.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.haproxy.org/download/2.2/src/%{name}-%{version}.tar.gz
%define sha512 %{name}=b9afa4a4112dccaf192fce07b1cdbb1547060d998801595147a41674042741b62852f65a65aa9b2d033db8808697fd3a522494097710a19071fbb0c604544de5

Patch0: %{name}-CVE-2021-39242.patch
Patch1: %{name}-CVE-2021-39240.patch
Patch2: %{name}-CVE-2021-40346.patch
Patch3: %{name}-CVE-2022-0711.patch
Patch4: %{name}-CVE-2023-25725.patch
Patch5: %{name}-CVE-2023-0056.patch
Patch6: %{name}-CVE-2023-0836.patch

BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: lua-devel
BuildRequires: pkg-config
BuildRequires: zlib-devel
BuildRequires: systemd-devel

Requires: systemd

%description
HAProxy is a fast and reliable solution offering high availability, load
balancing, and proxying for TCP and HTTP-based applications. It is suitable
for very high traffic web-sites.

%package        doc
Summary:        Documentation for haproxy
%description    doc
It contains the documentation and manpages for haproxy package.
Requires:       %{name} = %{version}-%{release}

%prep
%autosetup -p1

%build
make %{?_smp_mflags} TARGET=linux-glibc USE_PCRE=1 USE_OPENSSL=1 \
        USE_GETADDRINFO=1 USE_ZLIB=1 USE_SYSTEMD=1 \
        EXTRA_OBJS="contrib/prometheus-exporter/service-prometheus.o" \
        ADDLIB="-Wl,--no-as-needed -lgcc_s -Wl,--as-needed"
make %{?_smp_mflags} -C contrib/systemd
sed -i s/"local\/"/""/g contrib/systemd/haproxy.service
sed -i "s/\/run/\/var\/run/g" contrib/systemd/haproxy.service
sed -i "s/192.168.1.22/127.0.0.0/g" examples/transparent_proxy.cfg

%install
make DESTDIR=%{buildroot} PREFIX=%{_prefix} DOCDIR=%{_docdir}/haproxy TARGET=linux2628 install %{?_smp_mflags}
install -vDm755 contrib/systemd/haproxy.service \
       %{buildroot}/usr/lib/systemd/system/haproxy.service
install -vDm644 examples/transparent_proxy.cfg  %{buildroot}/%{_sysconfdir}/haproxy/haproxy.cfg

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/systemd/system/haproxy.service
%config(noreplace) %{_sysconfdir}/haproxy/haproxy.cfg

%files doc
%defattr(-,root,root,-)
%{_docdir}/haproxy/*
%{_mandir}/*

%changelog
* Wed Apr 05 2023 Nitesh Kumar <kunitesh@vmware.com> 2.2.6-6
- Fix CVE-2023-0056, CVE-2023-0836
* Mon Feb 27 2023 Harinadh D <hdommaraju@vmware.com> 2.2.6-5
- fix CVE-2023-25725
* Tue Mar 15 2022 Nitesh Kumar <kunitesh@vmware.com> 2.2.6-4
- Fix CVE-2022-0711
* Fri Sep 17 2021 Nitesh Kumar <kunitesh@vmware.com> 2.2.6-3
- Fix CVE-2021-40346
* Tue Aug 31 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.2.6-2
- Fix CVE CVE-2021-39242, CVE-2021-39240
* Mon Dec 14 2020 Gerrit Photon <photon-checkins@vmware.com> 2.2.6-1
- Automatic Version Bump
* Wed Aug 05 2020 Andrew Kutz <akutz@vmware.com> 2.2.2-1
- Update to version 2.2.2
- Removed patch for CVE-2020-11100 as it is now built into the program
* Wed Aug 05 2020 Andrew Kutz <akutz@vmware.com> 2.1.0-2
- Build with --no-as-needed to fix error dynamically loading pthread_cancel
* Tue Apr 14 2020 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.0-1
- Update to 2.1.0, add prometheus support
* Mon Apr 06 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.0.10-2
- Fix CVE-2020-11100
* Tue Dec 17 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.0.10-1
- Update to version 2.0.10 to fix CVE-2019-19330
* Thu Oct 31 2019 Shreyas B. <shreyasb@vmware.com> 2.0.3-2
- Fixes for CVE-2019-18277
* Mon Aug 12 2019 Kuladeep Rayalla <krayalla@vmware.com> 2.0.3-1
- Update to version 2.0.3
* Tue Apr 16 2019 Siju Maliakkal <smaliakkal@vmware.com> 1.8.14-3
- Applied patch for CVE-2018-20615
* Thu Feb 28 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.14-2
- Patch for CVE_2018_20102
- Patch for CVE_2018_20103
* Tue Dec 04 2018 Ajay Kaher <akaher@vmware.com> 1.8.14-1
- Update to version 1.8.14
* Thu Oct 25 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 1.8.13-2
- Build with USE_SYSTEMD=1 to fix service startup.
* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 1.8.13-1
- Update to version 1.8.13
* Tue Apr 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.6.12-1
- Updated to version 1.6.12
* Sun Nov 27 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.6.10-1
- Upgrade to 1.6.10 to address CVE-2016-5360
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.3-3
- GA - Bump release of all rpms
* Fri May 20 2016 Xiaolin Li <xiaolinl@vmware.com> 1.6.3-2
- Add haproxy-systemd-wrapper to package, add a default configuration file.
* Mon Feb 22 2016 Xiaolin Li <xiaolinl@vmware.com> 1.6.3-1
- Updated to version 1.6.3
* Thu Oct 01 2015 Vinay Kulkarni <kulkarniv@vmware.com> 1.5.14-1
- Add haproxy v1.5 package.
