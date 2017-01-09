Summary:        unbound dns server
Name:           unbound
Version:        1.6.0
Release:        1%{?dist}
Group:          System/Servers
Vendor:         VMware, Inc.
License:        BSD
Distribution:   Photon
URL:            http://www.unbound.net
Source0:        https://www.unbound.net/downloads/%{name}-%{version}.tar.gz
%define sha1 unbound=9b7606b016b447dc837efc108cee94f3fecf4ede
Source1:        %{name}.service
Requires:       shadow
Requires:       systemd
BuildRequires:  systemd

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
%{_sysconfdir}/*
%{_unitdir}/%{name}.service

%files devel
%{_includedir}/*
%{_libdir}/*.so

%files docs
%{_mandir}/*

%changelog
*  Fri Jan 06 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.0-1
-  Initial
