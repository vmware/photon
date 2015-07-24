Summary:	Usermode tools for VmWare virts
Name:		open-vm-tools
Version:	10.0.0
Release:	1%{?dist}
License:	LGPLv2+
URL:		https://github.com/vmware/open-vm-tools/archive/stable-10.0.0.tar.gz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	%{name}-%{version}.tar.gz
%define sha1 open-vm-tools=ff6421f75409f847f74f1f1fdb7e5bad4e74fe0b
Source1:        gosc-scripts.tar.gz
%define sha1 gosc-scripts=a87bb5b95f78923ac6053513b3364a119795a5d0
Patch0:		open-vm-tools-service-link.patch
Patch1:         open-vm-tools-GOSC-photon.patch
Patch2:         open-vm-tools-GOSC-vca.patch
BuildRequires: 	glib-devel
BuildRequires: 	xerces-c-devel
BuildRequires: 	xml-security-c-devel
BuildRequires: 	libdnet
BuildRequires: 	libmspack
BuildRequires:	Linux-PAM
BuildRequires:	openssl-devel
BuildRequires:	procps-ng-devel
Requires:	xerces-c
Requires:	libdnet
Requires:	libmspack
Requires:	glib
Requires:	xml-security-c
Requires:	openssl
%description
VmWare virtualization user mode tools
%prep
%setup -q
%setup -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p0
%build
autoreconf -i
./configure --prefix=/usr --without-x --without-kernel-modules --without-icu --disable-static
make %{?_smp_mflags}
%install

#collecting hacks to manually drop the vmhgfs module
install -vdm 755 %{buildroot}/lib/systemd/system
install -vdm 755 %{buildroot}/usr/share/open-vm-tools/GOSC/
cp -r gosc-scripts %{buildroot}/usr/share/open-vm-tools/GOSC

#stuff to enable vmtoolsd service
cat >> %{buildroot}/lib/systemd/system/vmtoolsd.service <<-EOF
[Unit]
Description=Service for virtual machines hosted on VMware
Documentation=http://open-vm-tools.sourceforge.net/about.php
ConditionVirtualization=vmware

[Service]
ExecStart=/usr/bin/vmtoolsd
TimeoutStopSec=5

[Install]
WantedBy=multi-user.target
EOF


make DESTDIR=%{buildroot} install
rm -f %{buildroot}/sbin/mount.vmhgfs
%post
ln -s /usr/sbin/mount.vmhgfs /sbin/mount.vmhgfs
/sbin/ldconfig
/bin/systemctl enable vmtoolsd
%postun	-p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_libdir}/open-vm-tools/plugins/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_bindir}/*
%{_sysconfdir}/*
%{_datadir}/*
%{_prefix}/etc/*
/lib/*
%{_sbindir}/*


%changelog
*       Thu Jul 23 2015 Anish Swaminathan <anishs@vmware.com> 10.0.0-1
        Update vm tools version.
*       Thu Jul 09 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-4
        Fixing GOSC to work on VCA.
*       Tue Apr 21 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-3
        Adding guest optimizations support for photon.
*	Tue Apr 21 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.0-2
	Added open-vm-tools-stderr_r-fix upstream patch and removed glibc patch.
*	Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 9.10.0-1
	Initial version
