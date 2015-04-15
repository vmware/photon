Summary:	Git for operating system binaries
Name:		ostree
Version:	2015.3
Release:	1
Source0:	http://ftp.gnome.org/pub/GNOME/sources/ostree/%{version}/%{name}-%{version}.tar.xz
Source1:	91-ostree.preset
Patch0:		ostree_syntax_error_fix.patch
License:	LGPLv2+
URL:		http://live.gnome.org/OSTree
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	which
BuildRequires:	libgsystem
BuildRequires:	xz-devel
BuildRequires:	gtk-doc
BuildRequires:	e2fsprogs-devel
Requires:	libgsystem
BuildRequires:	attr
BuildRequires:	python2-libs
BuildRequires:	python2
BuildRequires:	gobject-introspection
BuildRequires:	gobject-introspection-python

%description
OSTree is a tool for managing bootable, immutable, versioned
filesystem trees. While it takes over some of the roles of tradtional
"package managers" like dpkg and rpm, it is not a package system; nor
is it a tool for managing full disk images. Instead, it sits between
those levels, offering a blend of the advantages (and disadvantages)
of both.

%prep
%setup -q 
pwd
%patch0 -p0
%build
env NOCONFIGURE=1 ./autogen.sh
%configure \
	--disable-silent-rules \
	--enable-gtk-doc \
	--prefix=%{_prefix}
	  
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p -c"
find %{buildroot} -name '*.la' -delete
install -D -m 0644 %{SOURCE1} %{buildroot}/%{_prefix}/lib/systemd/system-preset/91-ostree.preset

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
%{_mandir}/man1/*.gz
%{_prefix}/lib/systemd/system-preset/91-ostree.preset
%dir %{_datadir}/gtk-doc/html/ostree
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_sysconfdir}/grub.d/*ostree
%{_libexecdir}/ostree/grub2*
%{_datadir}/gtk-doc/html/ostree/*
%changelog
*	Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 2014.11-1
-	Initial build. First version

