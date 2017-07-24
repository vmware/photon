Summary:        Linux kernel packet control tool
Name:           iptables
Version:        1.6.1
Release:        3%{?dist}
License:        GPLv2+
URL:            http://www.netfilter.org/projects/iptables
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.netfilter.org/projects/iptables/files/%{name}-%{version}.tar.bz2
%define sha1    iptables-=b2592490ca7a6c2cd0f069e167a4337c86acdf91
Source1:        iptables.service
Source2:        iptables
Source3:        iptables.stop
Source4:        ip4save
Source5:        ip6save
BuildRequires:  systemd
Requires:       systemd
%description
The next part of this chapter deals with firewalls. The principal 
firewall tool for Linux is Iptables. You will need to install 
Iptables if you intend on using any form of a firewall.

%package        devel
Summary:        Header and development files for iptables
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications.

%prep
%setup -q
%build
./configure \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --disable-silent-rules \
    --prefix=%{_prefix} \
    --exec-prefix= \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --with-xtlibdir=%{_libdir}/iptables \
    --with-pkgconfigdir=%{_libdir}/pkgconfig \
    --disable-nftables \
    --enable-libipq \
    --enable-devel

make V=0
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
ln -sfv ../../sbin/xtables-multi %{buildroot}%{_libdir}/iptables-xml
#   Install daemon scripts
install -vdm755 %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -vdm755 %{buildroot}/etc/systemd/scripts
install -m 755 %{SOURCE2} %{buildroot}/etc/systemd/scripts
install -m 755 %{SOURCE3} %{buildroot}/etc/systemd/scripts
install -m 644 %{SOURCE4} %{buildroot}/etc/systemd/scripts
install -m 644 %{SOURCE5} %{buildroot}/etc/systemd/scripts

find %{buildroot} -name '*.a'  -delete
find %{buildroot} -name '*.la' -delete
%{_fixperms} %{buildroot}/*

%preun
%systemd_preun iptables.service

%post
/sbin/ldconfig
%systemd_post iptables.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart iptables.service

%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%config(noreplace) /etc/systemd/scripts/iptables
%config(noreplace) /etc/systemd/scripts/iptables.stop
%config(noreplace) /etc/systemd/scripts/ip4save
%config(noreplace) /etc/systemd/scripts/ip6save
/lib/systemd/system/iptables.service
/sbin/*
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/iptables/*
%{_libdir}/iptables-xml
%{_mandir}/man1/*
%{_mandir}/man8/*

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man3/*

%changelog
*   Mon Jul 24 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.1-3
-   use iptables-restore to reload rules.
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 1.6.1-2
-   Add devel package.
*   Tue Mar 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.6.1-1
-   Updated to version 1.6.1
*   Wed Jan 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.6.0-6
-   Flush iptables on service stop
*   Tue Aug 30 2016 Anish Swaminathan <anishs@vmware.com> 1.6.0-5
-   Change config file properties for iptables script
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.0-4
-   GA - Bump release of all rpms
*   Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 1.6.0-3
-   Adding package support in pre/post/un scripts section.
*   Thu Apr 21 2016 Divya Thaluru <dthaluru@vmware.com> 1.6.0-2
-   Enabled iptable service. Added iptable rule to accept ssh connections by default.
*   Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.6.0-1
-   Updated to version 1.6.0
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  1.4.21-3
-   Add systemd to Requires and BuildRequires.
-   Use systemctl to enable/disable service.
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.4.21-2
-   Updated group.
*   Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 1.4.21-1
-   Initial build.  First version
