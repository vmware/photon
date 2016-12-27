Summary:        Linux kernel packet control tool
Name:           iptables
Version:        1.6.0
Release:        6%{?dist}
License:        GPLv2+
URL:            http://www.netfilter.org/projects/iptables
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.netfilter.org/projects/iptables/files/%{name}-%{version}.tar.bz2
%define sha1    iptables=21a694e75b0d6863cc001f85fb15915d12b8cc22
Source1:        http://www.linuxfromscratch.org/blfs/downloads/systemd/blfs-systemd-units-20140907.tar.bz2
%define sha1    blfs-systemd-units=713afb3bbe681314650146e5ec412ef77aa1fe33
Source2:        iptable_rules
Patch1:         blfs_systemd_fixes.patch
BuildRequires:  systemd
Requires:       systemd
%description
The next part of this chapter deals with firewalls. The principal 
firewall tool for Linux is Iptables. You will need to install 
Iptables if you intend on using any form of a firewall.

%package devel
Summary:        Development headers for iptables
Requires:       %{name} = %{version}-%{release}

%description devel
The iptables-devel package contains libraries, header files and documentation
for developing applications that use iptables.

%prep
%setup -q
tar xf %{SOURCE1} --no-same-owner
cp %{SOURCE2} .
%patch1 -p0
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
#   Install daemon script
pushd blfs-systemd-units-20140907
make DESTDIR=%{buildroot} install-iptables
popd
install -vdm755 %{buildroot}/etc/systemd/scripts
cp iptable_rules %{buildroot}/etc/systemd/scripts/iptables
chmod 755 %{buildroot}/etc/systemd/scripts/iptables
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
/lib/systemd/system/iptables.service
/sbin/*
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/iptables/*
%{_libdir}/iptables-xml
%{_mandir}/man1/*
%{_mandir}/man8/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man3/*

%changelog
*   Wed Dec 21 2016 Xiaolin Li <xiaolinl@vmware.com> 1.6.0-6
-   Add devel subpackage.
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
