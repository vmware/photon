Summary:	Virtualization API library that supports KVM, QEMU, Xen, ESX etc
Name:		libvirt
Version:	3.0.0
Release:	1%{?dist}
License:	LGPL
URL:		http://libvirt.org/
Source0:	http://libvirt.org/sources/%{name}-%{version}.tar.xz
%define sha1 libvirt=8a38fd5a0538a8ac05c8e4722bc4015c51237be0
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
BuildRequires:  systemd-devel
BuildRequires:  parted
BuildRequires:  python2-devel
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
/etc/libvirt/*
/etc/logrotate.d/libvirtd*
/etc/sasl2/libvirt.conf
%{_sysconfdir}/*
%{_libdir}/libvirt*
%{_libdir}/sysctl.d/60-libvirtd.conf
%{_libdir}/systemd/system/*
/usr/libexec/libvirt*
%{_sbindir}/*

%files devel
%{_includedir}/libvirt/*
%{_libdir}/pkgconfig/libvirt*

%files docs
/usr/share/augeas/lenses/*
/usr/share/doc/*
/usr/share/doc/libvirt-3.0.0/*
/usr/share/gtk-doc/*
/usr/share/libvirt/*
/usr/share/locale/*
%{_mandir}/*

%changelog
*    Fri Feb 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.0.0-1
-    Initial version of libvirt package for Photon.
