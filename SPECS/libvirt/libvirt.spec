Summary:	Virtualization API library that supports KVM, QEMU, Xen, ESX etc
Name:		libvirt
Version:	3.2.0
Release:	1%{?dist}
License:	LGPL
URL:		http://libvirt.org/
Source0:	http://libvirt.org/sources/%{name}-%{version}.tar.xz
%define sha1 libvirt=47d4b443fdf1e268589529018c436bbc4b413a7c
Group:		Virtualization/Libraries
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildRequires:  cyrus-sasl
BuildRequires:  device-mapper-devel
BuildRequires:  gnutls-devel
BuildRequires:  libxml2-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  libcap-ng-devel
BuildRequires:  libnl-devel
BuildRequires:  libselinux-devel
BuildRequires:  libssh2-devel
BuildRequires:  openssl-devel
BuildRequires:  systemd
BuildRequires:  parted
BuildRequires:  python2-devel
BuildRequires:  readline
BuildRequires:  readline-devel
Requires:       cyrus-sasl
Requires:       device-mapper
Requires:       gnutls
Requires:       libxml2
Requires:       e2fsprogs
Requires:       libcap-ng
Requires:       libnl
Requires:       libselinux
Requires:       libssh2
Requires:       systemd
Requires:       parted
Requires:       python2
Requires:       readline

%description
Libvirt is collection of software that provides a convenient way to manage virtual machines and other virtualization functionality, such as storage and network interface management. These software pieces include an API library, a daemon (libvirtd), and a command line utility (virsh).  An primary goal of libvirt is to provide a single way to manage multiple different virtualization providers/hypervisors. For example, the command 'virsh list --all' can be used to list the existing virtual machines for any supported hypervisor (KVM, Xen, VMWare ESX, etc.) No need to learn the hypervisor specific tools!

%package docs
Summary:        libvirt docs
Group:          Development/Tools
%description docs
The contains libvirt package doc files.

%package devel
Summary:        libvirt devel
Group:          Development/Tools
%description devel
This contains development tools and libraries for libvirt.

%prep
%setup -q

%build
./configure \
	--disable-silent-rules \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
        --with-udev=no \
        --with-pciaccess=no

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libvirt*.so.*
%{_libdir}/libvirt/storage-backend/*
%{_libdir}/sysctl.d/60-libvirtd.conf
%{_libdir}/systemd/system/*
/usr/libexec/libvirt*
%{_sbindir}/*

%config(noreplace)%{_sysconfdir}/sasl2/libvirt.conf
%config(noreplace)%{_sysconfdir}/libvirt/*.conf
%{_sysconfdir}/libvirt/nwfilter/*
%{_sysconfdir}/libvirt/qemu/*
%{_sysconfdir}/logrotate.d/*
%{_sysconfdir}/sysconfig/*
%{_bindir}/*

%files devel
%{_includedir}/libvirt/*
%{_libdir}/libvirt*.so
%{_libdir}/libvirt/connection-driver/*.so
%{_libdir}/libvirt/lock-driver/*.so
%{_libdir}/pkgconfig/libvirt*
%{_libdir}/libvirt/storage-backend/*

%files docs
/usr/share/augeas/lenses/*
/usr/share/doc/%{name}-%{version}/*
/usr/share/gtk-doc/*
/usr/share/libvirt/*
/usr/share/locale/*
%{_mandir}/*

%changelog
*    Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com> 3.2.0-1
-    Upgrading version to 3.2.0
*    Fri Feb 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.0.0-1
-    Initial version of libvirt package for Photon.
