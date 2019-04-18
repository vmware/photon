Summary:        A fast, reliable HA, load balancing, and proxy solution.
Name:           haproxy
Version:        1.8.14
Release:        4%{?dist}
License:        GPL
URL:            http://www.haproxy.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.haproxy.org/download/1.8/src/%{name}-%{version}.tar.gz
%define sha1 haproxy=589c6f933d73e8d6ba5307c8304cafb80e968481
Patch0:         haproxy_CVE_2018_20102.patch
Patch1:         haproxy_CVE_2018_20103.patch
Patch2:		haproxy-CVE-2018-20615.patch
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  lua-devel
BuildRequires:  pkg-config
BuildRequires:  zlib-devel
BuildRequires:  systemd
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
%patch0 -p1
%patch1 -p1
%patch2 -p1

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
*   Wed Apr 17 2019 Siju Maliakkal <smaliakkal@vmware.com> 1.8.14-4
-   Patch for CVE-2018-20615
*   Thu Feb 28 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.14-3
-   Patch for CVE_2018_20102
-   Patch for CVE_2018_20103
*   Tue Jan 29 2019 Ajay Kaher <akaher@vmware.com> 1.8.14-2
-   Build with USE_SYSTEMD=1 to fix service startup
*   Tue Dec 04 2018 Ajay Kaher <akaher@vmware.com> 1.8.14-1
-   Update to version 1.8.14
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

