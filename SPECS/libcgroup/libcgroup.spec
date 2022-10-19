Summary:      Library to control and monitor control groups
Name:         libcgroup
Version:      3.0.0
Release:      1%{?dist}
Group:        Development/Libraries
Distribution: Photon
Vendor:       VMware, Inc.
License:      LGPLv2+
URL:          http://libcg.sourceforge.net/
Source0:      https://github.com/libcgroup/libcgroup/archive/%{name}-%{version}.tar.gz
%define  sha512 %{name}=1e8a7c9a71d928ab0e354254b007b30fc159a30e441bd52a03ded142420c94e130594bb512680c62fc22f5193934fb78afc31453342b032d1db3197fd4c3e606
Source1:      cgconfig.service
Patch0:       photon-config.patch

BuildRequires: byacc, flex
BuildRequires: Linux-PAM-devel
BuildRequires: systemd-devel

%description
Control groups infrastructure. The library helps manipulate, control,
administrate and monitor control groups and the associated controllers.

%package tools
Summary: Command-line utility programs, services and daemons for libcgroup
Requires: %{name} = %{version}-%{release}
Requires: systemd

%description tools
This package contains command-line programs, services and a daemon for
manipulating control groups using the libcgroup library.

%package pam
Summary: A Pluggable Authentication Module for libcgroup
Requires: %{name} = %{version}-%{release}
Requires: Linux-PAM

%description pam
Linux-PAM module, which allows administrators to classify the user's login
processes to pre-configured control group.

%package devel
Summary: Development libraries to develop applications that utilize control groups
Requires: %{name} = %{version}-%{release}

%description devel
It provides API to create/delete and modify cgroup nodes. It will also in the
future allow creation of persistent configuration for control groups and
provide scripts to manage that configuration.

%prep
# Using autosetup is not feasible
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .config-patch

%build
autoreconf -vif
%configure --enable-pam-module-dir=%{_libdir}/security \
           --enable-opaque-hierarchy="name=systemd" \
           --disable-daemon

%make_build

%install
%make_install
# install config files
install -d %{buildroot}%{_sysconfdir}
install -m 644 samples/config/cgconfig.conf %{buildroot}/%{_sysconfdir}/cgconfig.conf
install -m 644 samples/config/cgsnapshot_blacklist.conf %{buildroot}/%{_sysconfdir}/cgsnapshot_blacklist.conf

# sanitize pam module, we need only pam_cgroup.so
rm -f %{buildroot}%{_libdir}/security/pam_cgroup.la
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/libcgroupfortesting.*

# install unit and sysconfig files
install -d %{buildroot}%{_unitdir}
install -m 644 %SOURCE1 %{buildroot}%{_unitdir}/
install -d %{buildroot}%{_sysconfdir}/sysconfig

%check
%if 0%{?with_check}
make %{?_smp_mflags} -C tests/gunit check
%endif

%post tools
%systemd_post cgconfig.service

%preun tools
%systemd_preun cgconfig.service

%postun tools
%systemd_postun_with_restart cgconfig.service

%files
%{!?_licensedir:%global license %%doc}
%{_libdir}/libcgroup.so.3*

%files tools
%config(noreplace) %{_sysconfdir}/cgconfig.conf
%config(noreplace) %{_sysconfdir}/cgsnapshot_blacklist.conf
%{_bindir}/cgcreate
%{_bindir}/cgget
%{_bindir}/cgset
%{_bindir}/cgxget
%{_bindir}/cgxset
%{_bindir}/cgdelete
%{_bindir}/lscgroup
%{_bindir}/lssubsys
%{_sbindir}/cgconfigparser
%{_bindir}/cgsnapshot
%{_bindir}/cgclassify
%attr(0755, root, root) %{_bindir}/cgexec
%attr(0644, root, root) %{_mandir}/man1/*
%attr(0644, root, root) %{_mandir}/man5/*
%attr(0644, root, root) %{_mandir}/man8/*
%{_unitdir}/cgconfig.service

%files pam
%attr(0755,root,root) %{_libdir}/security/pam_cgroup.so

%files devel
%{_includedir}/libcgroup.h
%{_includedir}/libcgroup/*.h
%{_libdir}/libcgroup.so
%{_libdir}/pkgconfig/libcgroup.pc
%{_libdir}/security/pam_cgroup.a
%{_libdir}/*.a

%changelog
* Tue Sep 13 2022 Roye Eshed <eshedr@vmware.com> - 3.0.0-1
- Creation of the libcgroup spec file for photon based on the Fedora SPEC file.
