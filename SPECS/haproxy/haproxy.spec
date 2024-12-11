Summary:        A fast, reliable HA, load balancing, and proxy solution.
Name:           haproxy
Version:        2.8.2
Release:        2%{?dist}
URL:            http://www.haproxy.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.haproxy.org/download/2.7/src/%{name}-%{version}.tar.gz
%define sha512 %{name}=717bbdd626d3c03c06ad237fe2cb46c71b7cddcf0ba40b6bedb66293a9db9655204f83848ada32dc28dd782b98c8ee32516f90203ac0273759f171e955b4527d

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 2.8.2-2
- Release bump for SRP compliance
* Fri Dec 08 2023 Nitesh Kumar <kunitesh@vmware.com> 2.8.2-1
- Version upgrade to v2.8.2 to fix CVE-2023-45539
* Mon Aug 21 2023 Nitesh Kumar <kunitesh@vmware.com> 2.7.10-1
- Version upgrade to v2.7.10 to fix CVE-2023-40225
* Tue Jun 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.7.3-2
- Bump version as a part of lua upgrade
* Thu May 18 2023 Nitesh Kumar <kunitesh@vmware.com> 2.7.3-1
- Version upgrade to v2.7.3 to fix CVE-2023-25725
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.7.0-3
- Bump version as a part of zlib upgrade
* Wed Apr 05 2023 Nitesh Kumar <kunitesh@vmware.com> 2.7.0-2
- Fix CVE-2023-0056, CVE-2023-0836
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 2.7.0-1
- Automatic Version Bump
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 2.6.6-1
- Automatic Version Bump
* Fri Sep 16 2022 Nitesh Kumar <kunitesh@vmware.com> 2.6.4-1
- Upgrade to v2.6.4
* Tue Mar 15 2022 Nitesh Kumar <kunitesh@vmware.com> 2.5.5-1
- Upgrade to 2.5.5, Address CVE-2022-0711
* Wed Nov 10 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.3.10-3
- openssl 3.0.0
* Fri Sep 17 2021 Nitesh Kumar <kunitesh@vmware.com> 2.3.10-2
- Fix CVE-2021-40346
* Thu May 06 2021 Gerrit Photon <photon-checkins@vmware.com> 2.3.10-1
- Automatic Version Bump
* Fri Feb 05 2021 Susant Sahani <ssahani@vmware.com> 2.3.4-1
- Version bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.2.2-2
- openssl 1.1.1
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.2.2-1
- Automatic Version Bump
* Thu Mar 05 2020 Ashwin H <ashwinh@vmware.com> 2.0.10-1
- Update to version 2.0.10 to fix CVE-2019-19330
* Thu Nov 7 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.0.6-1
- Update to 2.0.6
* Tue Apr 2 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-1
- Update to 1.9.6
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
