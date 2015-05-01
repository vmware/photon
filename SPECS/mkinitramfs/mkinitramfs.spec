Summary:    mkinitramfs
Name:       mkinitramfs
Version:    3.19.2
Release:    1
License:    GPLv2
URL:        http://www.vmware.com/
Group:      System Environment/Kernel
Vendor:     VMware, Inc.
Distribution: Photon
Source0:    http://www.vmware.com/%{name}-%{version}.tar.gz


BuildRequires: glibc
BuildRequires: zlib
BuildRequires: filesystem
BuildRequires: gmp
BuildRequires: mpfr
BuildRequires: libgcc
BuildRequires: libstdc++
BuildRequires: bzip2
BuildRequires: pkg-config
BuildRequires: ncurses
BuildRequires: cracklib
BuildRequires: cracklib-dicts
BuildRequires: shadow
BuildRequires: procps-ng
BuildRequires: e2fsprogs
BuildRequires: iana-etc
BuildRequires: readline
BuildRequires: coreutils
BuildRequires: bash
BuildRequires: bc
BuildRequires: libtool
BuildRequires: inetutils
BuildRequires: xz
BuildRequires: grub
BuildRequires: iproute2
BuildRequires: kbd
BuildRequires: kmod
BuildRequires: libpipeline
BuildRequires: util-linux
BuildRequires: openssl
BuildRequires: libffi
BuildRequires: expat
BuildRequires: linux
BuildRequires: curl
BuildRequires: iptables
BuildRequires: ca-certificates
BuildRequires: Linux-PAM
BuildRequires: attr
BuildRequires: libcap
BuildRequires: systemd
BuildRequires: dbus

%description
initrd file

%prep
%setup -q

%build
install -vdm 755 %{buildroot}/boot
./mkinitramfs -n %{buildroot}/boot/initramfs.img-no-kmods

%install

%check

%files
%defattr(-,root,root)
/boot/initramfs.img-no-kmods