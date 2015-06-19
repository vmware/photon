Summary:	Git for operating system binaries
Name:		ostree
Version:	2015.7
Release:	1%{?dist}
Source0:	http://ftp.gnome.org/pub/GNOME/sources/ostree/%{version}/%{name}-%{version}.tar.gz
Source1:	91-ostree.preset
#Patch0:		ostree_syntax_error_fix.patch
License:	LGPLv2+
URL:		http://live.gnome.org/OSTree
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	git
BuildRequires:	which
BuildRequires:	libgsystem
BuildRequires:	xz-devel
BuildRequires:	gtk-doc
BuildRequires:	e2fsprogs-devel
Requires:	libgsystem
Requires:	gpgme
Requires:	libassuan
Requires:	libgpg-error
Requires:       systemd
BuildRequires:	attr
BuildRequires:	python2-libs
BuildRequires:	python2
BuildRequires:	gobject-introspection
BuildRequires:	gobject-introspection-devel
BuildRequires:	gobject-introspection-python
BuildRequires:  gpgme-devel
BuildRequires:  libcap
BuildRequires:  systemd

%description
OSTree is a tool for managing bootable, immutable, versioned
filesystem trees. While it takes over some of the roles of tradtional
"package managers" like dpkg and rpm, it is not a package system; nor
is it a tool for managing full disk images. Instead, it sits between
those levels, offering a blend of the advantages (and disadvantages)
of both.

%package devel
Summary: Development headers for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package includes the header files for the %{name} library

%prep
%autosetup -Sgit -n %{name}-%{version}
git clone git://git.gnome.org/libglnx libglnx
git clone https://github.com/mendsley/bsdiff bsdiff

#pwd
#%patch0 -p0
%build
env NOCONFIGURE=1 ./autogen.sh
%configure \
	--disable-silent-rules \
	--enable-gtk-doc \
	--with-dracut \
	--with-mkinitcpio \
	--prefix=%{_prefix}
	  
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p -c"
find %{buildroot} -name '*.la' -delete
install -D -m 0644 %{SOURCE1} %{buildroot}%{_prefix}/lib/systemd/system-preset/91-ostree.preset
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/
cp -R %{buildroot}/lib/systemd/system/*.service %{buildroot}%{_prefix}/lib/systemd/system/
rm -rf %{buildroot}/lib

%clean
rm -rf %{buildroot}

%post
%systemd_post ostree-remount.service

%preun
%systemd_preun ostree-remount.service

%files
%doc COPYING README.md
%{_bindir}/ostree
%{_libdir}/*.so.1*
%{_sbindir}/*
%{_mandir}/man*/*.gz
%{_prefix}/lib/systemd/system-preset/91-ostree.preset
%{_prefix}/lib/systemd/system/ostree*.service
%dir %{_prefix}/lib/dracut/modules.d/*ostree
%{_prefix}/lib/dracut/modules.d/98ostree/*
%{_sysconfdir}/grub.d/*ostree
%{_sysconfdir}/dracut.conf.d/ostree.conf
%{_sysconfdir}/ostree-mkinitcpio.conf
%{_libdir}/girepository-*/OSTree-*.typelib
%{_libexecdir}/ostree/grub2*
%{_libdir}/initcpio/*
%{_libdir}/lib*.so
%dir %{_datadir}/gtk-doc/html/ostree

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/html/ostree/*
%{_datadir}/ostree/*
%{_datadir}/gir-1.0/OSTree-1.0.gir

%changelog
*	Wed Jun 17 2015 Anish Swaminathan <anishs@vmware.com> 2015.7-1
-	Updated the version
*	Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 2014.11-1
-	Initial build. First version

