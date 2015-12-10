Summary: Intel LLDP Agent
Name:    lldpad
Version: 1.0.1
Release: 3.git036e314%{?dist}
License: GPLv2
URL: http://open-lldp.org/
Source: %{name}-%{version}.tar.gz
%define sha1 lldpad=71e35298e926f0c03556cede4861dffa36928500
Group:      System Environment/Daemons
Vendor:     VMware, Inc.
Distribution:  Photon

BuildRequires: libconfig
BuildRequires: libnl-devel
BuildRequires: readline-devel

%description
The lldpad package comes with utilities to manage an LLDP interface with support for reading and configuring TLVs. TLVs and interfaces are individual controlled allowing flexible configuration for TX only, RX only, or TX/RX modes per TLV.

%prep
%setup -q -n open-lldp-036e314

%build
./bootstrap.sh
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install 
find %{buildroot} -name '*.la' -exec rm -f {} ';'
mkdir -p %{buildroot}/lib/systemd/system
mv %{buildroot}/%{_libdir}/systemd/system/lldpad.service \
   	%{buildroot}/lib/systemd/system/lldpad.service
mv %{buildroot}/%{_libdir}/systemd/system/lldpad.socket  \
	%{buildroot}/lib/systemd/system/lldpad.socket
install -vdm755 %{buildroot}/etc/systemd/system/multi-user.target.wants
ln -sfv ../../../../lib/systemd/system/lldpad.socket \
	%{buildroot}/etc/systemd/system/multi-user.target.wants/lldpad.socket


%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%{_sbindir}/*
%{_libdir}/liblldp_clif.so.*
%{_sysconfdir}/bash_completion.d/*
%{_mandir}/man3/*
%{_mandir}/man8/*
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/liblldp_clif.so
%{_sysconfdir}/systemd/system/multi-user.target.wants/lldpad.socket
/lib/systemd/system/lldpad.service
/lib/systemd/system/lldpad.socket


%changelog
*	Wed Dec 09 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 1.0.1-2
-	Updating the provided files by the package.

*	Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 1.0.1-1
-   Initial build.  First version
