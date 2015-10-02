Summary:        A fast, reliable HA, load balancing, and proxy solution.
Name:           haproxy
Version:        1.5.14
Release:        1%{?dist}
License:        GPL
URL:            http://www.haproxy.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.haproxy.org/download/1.5/src/%{name}-%{version}.tar.gz
%define sha1 haproxy=159f5beb8fdc6b8059ae51b53dc935d91c0fb51f
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  pkg-config
BuildRequires:  zlib-devel

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
        USE_GETADDRINFO=1 USE_ZLIB=1
make %{?_smp_mflags} -C contrib/systemd
sed -i s/"local\/"/""/g contrib/systemd/haproxy.service

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} PREFIX=%{_prefix} DOCDIR=%{_docdir}/haproxy install
install -vDm755 contrib/systemd/haproxy.service \
       %{buildroot}/usr/lib/systemd/system/haproxy.service

%files
%defattr(-,root,root)
%{_sbindir}/haproxy
%{_sbindir}/haproxy-systemd-wrapper
%{_libdir}/systemd/system/haproxy.service

%files doc
%defattr(-,root,root,-)
%{_docdir}/haproxy/*
%{_mandir}/*

%changelog
*       Thu Oct 01 2015 Vinay Kulkarni <kulkarniv@vmware.com> 1.5.14-1
-       Add haproxy v1.5 package.

