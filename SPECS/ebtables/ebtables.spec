Summary:        A filtering tool for a Linux-based bridging firewall.
Name:           ebtables
Version:        2.0.10
Release:        1%{?dist}
License:        GPLv2+
URL:            http://ebtables.netfilter.org/
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        ftp://ftp.netfilter.org/pub/ebtables/%{name}-v%{version}-4.tar.gz
%define sha1    ebtables=907d3b82329e8fbb7aaaa98049732bd8dab022f9
Source1:        ebtables_script
Source2:        ebtables.service
BuildRequires:  systemd
Requires:       systemd
%description
The ebtables program is a filtering tool for a Linux-based bridging firewall. It enables transparent filtering of network traffic passing through a Linux bridge. The filtering possibilities are limited to link layer filtering and some basic filtering on higher network layers. Advanced logging, MAC DNAT/SNAT and brouter facilities are also included.

%prep
%setup -q -n %{name}-v%{version}-4

%build
make %{?_smp_mflags} CFLAGS="${RPM_OPT_FLAGS}"

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} BINDIR=%{_sbindir} MANDIR=%{_mandir} install

mkdir -p %{buildroot}/%{_libdir}/systemd/system
install -vdm755 %{buildroot}/etc/systemd/scripts
install -m 755 %{SOURCE1} %{buildroot}/etc/systemd/scripts/ebtables
install -m 644 %{SOURCE2} %{buildroot}/%{_libdir}/systemd/system/ebtables.service

%preun
%systemd_preun ebtables.service

%post
/sbin/ldconfig
%systemd_post ebtables.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart ebtables.service

%check
make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%doc COPYING
%{_sbindir}/*
%{_mandir}/man8/*
%{_libdir}/*.so
%config(noreplace) %{_sysconfdir}/sysconfig/ebtables-config
%{_libdir}/systemd/system/*
%{_sysconfdir}/ethertypes
%{_sysconfdir}/systemd/scripts/ebtables
%exclude %{_sysconfdir}/rc.d/init.d/ebtables


%changelog
*   Mon May 15 2017 Xiaolin Li <xiaolinl@vmware.com>  2.0.10-2
-   Added systemd to Requires and BuildRequires.
*   Wed Jan 18 2017 Xiaolin Li <xiaolinl@vmware.com>  2.0.10-1
-   Initial build.
