Summary:	Usermode tools for VmWare virts
Name:		open-vm-tools
Version:	10.0.0
Release:	4%{?dist}
License:	LGPLv2+
URL:		https://github.com/vmware/open-vm-tools
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:    http://downloads.sourceforge.net/project/open-vm-tools/open-vm-tools-10.0.0.tar.gz
%define sha1 open-vm-tools=1658ab1b73438e746bb6f11f16fe570eaf753747
Source1:        gosc-scripts.tar.gz
%define sha1 gosc-scripts=a87bb5b95f78923ac6053513b3364a119795a5d0
Patch0:		open-vm-tools-service-link.patch
Patch1:         open-vm-tools-GOSC-photon.patch
Patch2:         GOSC-VCA.patch
Patch3:         GOSC-return-code.patch
BuildRequires: 	glib-devel
BuildRequires: 	xerces-c-devel
BuildRequires: 	xml-security-c-devel
BuildRequires: 	libdnet
BuildRequires: 	libmspack
BuildRequires:	Linux-PAM
BuildRequires:	openssl-devel
BuildRequires:	procps-ng-devel
BuildRequires:	fuse-devel
Requires:	fuse
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
%patch3 -p0
%build
touch ChangeLog
autoreconf -i
sh ./configure --prefix=/usr --without-x --without-kernel-modules --without-icu --disable-static
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

%preun
/bin/systemctl disable vmtoolsd

%postun	-p /sbin/ldconfig
rm -f /sbin/mount.vmhgfs

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
*       Thu Aug 20 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-4
-       Fixing GOSC-libdeploy return code problem.
*       Thu Aug 13 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-3
-       Combining all GOSC patches and adding support for lightwave.
*       Wed Aug 12 2015 Alexey Makhalov <amakhalov@vmware.com> 10.0.0-2
-       Build with fuse support.
*       Wed Aug 12 2015 Alexey Makhalov <amakhalov@vmware.com> 10.0.0-1
-       Update version to 10.0.0.
*       Tue Aug 11 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-7
-       VCA initial login password issue fix.
*       Wed Aug 05 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-6
-       Adding preun and post install commands.
*       Thu Jul 30 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-5
-       Adding Blob configuation support to GOSC scripts.
*       Thu Jul 09 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-4
-       Fixing GOSC to work on VCA.
*       Tue Apr 21 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-3
-       Adding guest optimizations support for photon.
*	Tue Apr 21 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.0-2
-       Added open-vm-tools-stderr_r-fix upstream patch and removed glibc patch.
*       Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 9.10.0-1
-       Initial version
