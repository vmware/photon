Summary:	Linux kernel packet control tool
Name:		iptables
Version:	1.4.21
Release:	2%{?dist}
License:	GPLv2+
URL:		http://www.netfilter.org/projects/iptables
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://www.netfilter.org/projects/iptables/files/%{name}-%{version}.tar.bz2
%define sha1 iptables=85d4160537546a23a7e42bc26dd7ee62a0ede4c8
Source1:	http://www.linuxfromscratch.org/blfs/downloads/systemd/blfs-systemd-units-20140907.tar.bz2
%define sha1 blfs-systemd-units=713afb3bbe681314650146e5ec412ef77aa1fe33
Source2:	iptable_rules
Patch1:		blfs_systemd_fixes.patch
%description
The next part of this chapter deals with firewalls. The principal 
firewall tool for Linux is Iptables. You will need to install 
Iptables if you intend on using any form of a firewall.
%prep
%setup -q
tar xf %{SOURCE1}
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
	--enable-libipq \
	--enable-devel
	
make V=0 %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
ln -sfv ../../sbin/xtables-multi %{buildroot}%{_libdir}/iptables-xml
#	Install daemon script
pushd blfs-systemd-units-20140907
make DESTDIR=%{buildroot} install-iptables
popd
install -vdm755 %{buildroot}/etc/systemd/system/multi-user.target.wants
ln -sfv ../../../../lib/systemd/system/iptables.service  %{buildroot}/etc/systemd/system/multi-user.target.wants/iptables.service
install -vdm755 %{buildroot}/etc/systemd/scripts
cp iptable_rules %{buildroot}/etc/systemd/scripts/iptables
find %{buildroot} -name '*.a'  -delete
find %{buildroot} -name '*.la' -delete
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/etc/systemd/scripts/iptables
/etc/systemd/system/multi-user.target.wants/iptables.service
/lib/systemd/system/iptables.service
/sbin/*
%{_bindir}/*
%{_libdir}/*.so*
%{_libdir}/iptables/*
%{_libdir}/pkgconfig/*
%{_libdir}/iptables-xml
%{_includedir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man8/*
%changelog
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.4.21-2
-   Updated group.
*	Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 1.4.21-1
-	Initial build.	First version
