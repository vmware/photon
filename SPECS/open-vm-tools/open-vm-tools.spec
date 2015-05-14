Summary:	Usermode tools for VmWare virts
Name:		open-vm-tools
Version:	9.10.0
Release:	1
License:	LGPLv2+
URL:		https://github.com/vmware/open-vm-tools/archive/stable-9.10.x.zip
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://downloads.sourceforge.net/project/open-vm-tools/open-vm-tools/stable-9.10.0/%{name}-%{version}.tar.gz
Patch0:		open-vm-tools-glibc-fixes.patch
Patch1:		open-vm-tools-service-link.patch
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
%patch0 -p1
%patch1 -p1
%build
export CFLAGS="$RPM_OPT_FLAGS -Wno-unused-local-typedefs -Wno-deprecated-declarations -D_DEFAULT_SOURCE"
export CXXFLAGS="$RPM_OPT_FLAGS -Wno-unused-local-typedefs -Wno-deprecated-declarations -D_DEFAULT_SOURCE"
./configure --prefix=/usr --without-x --without-kernel-modules --without-icu --disable-static
make %{?_smp_mflags}
%install

#collecting hacks to manually drop the vmhgfs module
install -vdm 755 %{buildroot}/lib/systemd/system

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
*	Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 9.10.0-1
	Initial version
