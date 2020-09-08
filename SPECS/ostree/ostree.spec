Summary:        Git for operating system binaries
Name:           ostree
Version:        2020.6
Release:        1%{?dist}
License:        LGPLv2+
URL:            https://ostree.readthedocs.io/en/latest
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
# Manually created Source tar which is equal to
# Source0 + .git as it requires git hooks at build time
Source0:        https://github.com/ostreedev/ostree/archive/%{name}-%{version}.tar.gz
%define sha1    %{name}-%{version}=64d0a49d299342877ed5744e3e80133e7962bb31
Source1:        91-ostree.preset
Patch0:         dualboot-support.patch
Patch1:         0001-ostree-Copying-photon-config-to-boot-directory.patch
Patch2:         0002-ostree-Adding-load-env-to-menuentry.patch

BuildRequires:  git
BuildRequires:  autoconf automake libtool which
BuildRequires:  gtk-doc
BuildRequires:  glib-devel
BuildRequires:  gobject-introspection
BuildRequires:  gobject-introspection-devel
BuildRequires:  xz-devel
BuildRequires:  icu-devel
BuildRequires:  sqlite-devel
BuildRequires:  mkinitcpio
BuildRequires:  e2fsprogs-devel
BuildRequires:  libpsl-devel
BuildRequires:  zlib-devel
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  libsoup-devel
BuildRequires:  attr-devel
BuildRequires:  libarchive-devel
BuildRequires:  fuse-devel
BuildRequires:  libcap-devel
BuildRequires:  gpgme-devel
BuildRequires:  systemd-devel
BuildRequires:  dracut
BuildRequires:  bison
BuildRequires:  libselinux-devel

Requires: dracut
Requires: systemd
Requires: libassuan
Requires: gpgme
Requires: python3-gobject-introspection
Requires: libselinux

%description
OSTree is a tool for managing bootable, immutable, versioned
filesystem trees. While it takes over some of the roles of tradtional
"package managers" like dpkg and rpm, it is not a package system; nor
is it a tool for managing full disk images. Instead, it sits between
those levels, offering a blend of the advantages (and disadvantages)
of both.

%package libs
Summary: Development headers for %{name}
Group: Development/Libraries
Requires: libpsl
Requires: libsoup
Requires: icu


%description libs
The %{name}-libs provides shared libraries for %{name}.

%package devel
Summary: Development headers for %{name}
Group: Development/Libraries
Requires: %{name}-libs

%description devel
The %{name}-devel package includes the header files for the %{name} library.

%package grub2
Summary: GRUB2 integration for OSTree
Group: Development/Libraries
Requires: grub2
Requires: grub2-efi
Requires: %{name}

%description grub2
GRUB2 integration for OSTree

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
env NOCONFIGURE=1 ./autogen.sh
%configure \
     --disable-silent-rules \
     --enable-gtk-doc \
     --with-dracut \
     --with-mkinitcpio \
     --with-selinux \
     --enable-libsoup-client-certs
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} INSTALL="install -p -c" install
find %{buildroot} -name '*.la' -delete
install -D -m 0644 %{SOURCE1} %{buildroot}%{_libdir}/systemd/system-preset/91-ostree.preset
install -vdm 755 %{buildroot}/etc/ostree/remotes.d

%post
%systemd_post ostree-remount.service

%preun
%systemd_preun ostree-remount.service

%postun
%systemd_postun_with_restart ostree-remount.service

%files
%doc COPYING
%doc README.md
%{_bindir}/ostree
%{_bindir}/rofiles-fuse
%{_datadir}/ostree
%{_libdir}/initcpio/*
%dir %{_libdir}/dracut/modules.d/98ostree
%{_libdir}/systemd/system/ostree-finalize-staged.path
%{_libdir}/dracut/modules.d/98ostree/*
%{_libdir}/systemd/system-generators/ostree-system-generator
%{_libdir}/systemd/system-preset/91-ostree.preset
%{_libdir}/systemd/system/ostree*.service
%{_libdir}/ostree/ostree-prepare-root
%{_libdir}/ostree/ostree-remount
%{_libdir}/tmpfiles.d/ostree-tmpfiles.conf
%config(noreplace) %{_sysconfdir}/dracut.conf.d/ostree.conf
%config(noreplace) %{_sysconfdir}/ostree-mkinitcpio.conf
%{_mandir}/man1/ostree-admin*
%{_libexecdir}/libostree/*
%exclude %{_sysconfdir}/grub.d/*ostree
%exclude %{_libexecdir}/libostree/grub2*

%files libs
%{_sysconfdir}/ostree
%{_libdir}/*.so.1*
%{_libdir}/girepository-1.0/OSTree-1.0.typelib

%files devel
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_prefix}/share/bash-completion/completions/ostree
%{_datadir}/gtk-doc/html/ostree
%{_datadir}/gir-1.0/OSTree-1.0.gir
%exclude %{_mandir}/man1/ostree-admin*
%{_mandir}/man1/*.gz
%{_mandir}/man5/*.gz

%files grub2
%{_sysconfdir}/grub.d/*ostree
%{_libexecdir}/libostree/grub2*

%changelog
*   Thu Sep 03 2020 Ankit Jain <ankitja@vmware.com> 2020.6-1
-   Updated to 2020.6
*   Thu Aug 13 2020 Ankit Jain <ankitja@vmware.com> 2020.4-1
-   Updated to 2020.4
*   Mon Jun 22 2020 Tapas Kundu <tkundu@vmware.com> 2019.2-4
-   Build with gobject-introspection-python3
*   Thu Oct 24 2019 Ankit Jain <ankitja@vmware.com> 2019.2-3
-   Added for ARM Build
*   Fri Sep 13 2019 Ankit Jain <ankitja@vmware.com> 2019.2-2
-   Added support to get kernel and systemd commandline param
-   from photon.cfg and systemd.cfg
*   Tue May 14 2019 Ankit Jain <ankitja@vmware.com> 2019.2-1
-   Initial build. First version
