Summary:        A fast, reliable HA, load balancing, and proxy solution.
Name:           haproxy
Version:        1.9.6
Release:        1%{?dist}
License:        GPL
URL:            http://www.haproxy.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.haproxy.org/download/1.9/src/%{name}-%{version}.tar.gz
%define sha1 haproxy=0a9692836d4fc89df3a26002ed66af0f32459638
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
%description    doc
It contains the documentation and manpages for haproxy package.
Requires:       %{name} = %{version}-%{release}

%prep
%setup -q

%build
make %{?_smp_mflags} TARGET=linux2628 USE_PCRE=1 USE_OPENSSL=1 \
        USE_GETADDRINFO=1 USE_ZLIB=1 USE_SYSTEMD=1
make %{?_smp_mflags} -C contrib/systemd
sed -i s/"local\/"/""/g contrib/systemd/haproxy.service
sed -i "s/\/run/\/var\/run/g" contrib/systemd/haproxy.service
sed -i "s/192.168.1.22/127.0.0.0/g" examples/transparent_proxy.cfg

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} PREFIX=%{_prefix} DOCDIR=%{_docdir}/haproxy TARGET=linux2628 install
install -vDm755 contrib/systemd/haproxy.service \
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
