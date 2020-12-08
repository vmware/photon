Summary:	Team driver
Name:		libteam
Version:	1.31
Release:	1%{?dist}
License:        GPLv2+
URL:            http://www.libteam.org
Source0:        http://libteam.org/files/%{name}-%{version}.tar.gz
%define sha1 libteam=338f2bae08e143bc3f7a84317ddc3053cff2691d
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
BuildRequires:	libnl-devel
BuildRequires:	libdaemon-devel
BuildRequires:	jansson-devel
Distribution:	Photon
%description
The libteam package contains the user-space components of the Team driver. It provides a mechanism to team multiple NICs into one logical port at the L2 layer.

%package devel
Summary:	Development libraries and header files for libteam
Requires:	%{name} = %{version}-%{release}

%description devel
The package contains libraries and header files for
developing applications that use libteam

%package -n teamd
Summary:        Team network device control daemon
Requires:       %{name} = %{version}-%{release}

%description -n teamd
The teamd package contains the team network device control daemon

%package -n teamd-devel
Summary:        Development files for teamd
Requires:       %{name} = %{version}-%{release}

%description -n teamd-devel
The package contains libraries and header files for
developing applications that use teamd and libteamdctl

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -D -m 0644 teamd/redhat/systemd/teamd@.service  %{buildroot}%{_unitdir}/teamd@.service
install -p -m 755 utils/bond2team %{buildroot}%{_bindir}/bond2team
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifup-Team %{buildroot}%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifdown-Team %{buildroot}%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifup-TeamPort %{buildroot}%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifdown-TeamPort %{buildroot}%{_sysconfdir}/sysconfig/network-scripts
mkdir -p %{buildroot}%{_datadir}/teamd/example_configs/
install -p -m 644 teamd/example_configs/* %{buildroot}%{_datadir}/teamd/example_configs/

%post
/sbin/ldconfig

%preun
%systemd_preun teamd@.service

%postun
/sbin/ldconfig
%systemd_postun teamd@.service

%files
%defattr(-,root,root)
%{_libdir}/libteam.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/team.h
%{_libdir}/libteam.a
%{_libdir}/libteam.la
%{_libdir}/libteam.so
%{_libdir}/pkgconfig/libteam.pc

%files -n teamd
%{_libdir}/libteamdctl.so.*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_sysconfdir}/*
%{_unitdir}/teamd@.service

%files -n teamd-devel
%{_includedir}/teamdctl.h
%{_libdir}/libteamdctl.a
%{_libdir}/libteamdctl.la
%{_libdir}/libteamdctl.so
%{_libdir}/pkgconfig/libteamdctl.pc
%{_datadir}/teamd/*

%changelog
*   Tue Dec 08 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.31-1
-   Initial build. First version
