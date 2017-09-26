Summary:        unbound dns server
Name:           unbound
Version:        1.6.0
Release:        2%{?dist}
Group:          System/Servers
Vendor:         VMware, Inc.
License:        BSD
Distribution:   Photon
URL:            http://www.unbound.net
Source0:        https://www.unbound.net/downloads/%{name}-%{version}.tar.gz
%define sha1 unbound=9b7606b016b447dc837efc108cee94f3fecf4ede
Source1:        %{name}.service
Requires:       expat
Requires:       openssl
Requires:       shadow
Requires:       systemd
BuildRequires:  systemd
BuildRequires:  openssl-devel
BuildRequires:  expat

%description
Unbound is a validating, recursive, and caching DNS resolver.

%package	devel
Summary:	unbound development libs and headers
Group:		Development/Libraries

%description devel
Development files for unbound dns server

%package	docs
Summary:	unbound docs
Group:		Documentation

%description docs
unbound dns server docs

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --sysconfdir=%{_sysconfdir} \
    --with-conf-file=%{_sysconfdir}/%{name}/unbound.conf \
    --disable-static

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
find %{buildroot} -name '*.la' -delete
install -vdm755 %{buildroot}%{_unitdir}
install -pm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%check
make check

%pre
getent group unbound >/dev/null || groupadd -r unbound
getent passwd unbound >/dev/null || \
useradd -r -g unbound -d %{_sysconfdir}/unbound -s /sbin/nologin \
-c "Unbound DNS resolver" unbound

%post
    /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_sbindir}/*
%config(noreplace) %{_sysconfdir}/unbound/unbound.conf
%{_unitdir}/%{name}.service

%files devel
%{_includedir}/*
%{_libdir}/*.so

%files docs
%{_mandir}/*

%changelog
*  Tue Sep 26 2017 Anish Swaminathan <anishs@vmware.com> 1.6.0-2
-  Release bump for expat version update
*  Fri Jan 06 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.0-1
-  Initial
