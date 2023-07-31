Summary:        Git for operating system binaries
Name:           ostree
Version:        2019.2
Release:        5%{?dist}
License:        LGPLv2+
URL:            https://ostree.readthedocs.io/en/latest
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

# Manually created Source tar which is equal to
# Source0 + .git as it requires git hooks at build time
Source0: https://github.com/ostreedev/ostree/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=e8312d1926cb295ac17324dfee9f09a10c1aca2800334fed025b696152f88ed4b4e60226794036b65062f247667cd2f1c14c68a277598ea14873524ee1c344cd

Source1: 91-%{name}.preset

Patch0: dualboot-support.patch
Patch1: 0001-ostree-Copying-photon-config-to-boot-directory.patch
Patch2: 0002-ostree-Adding-load-env-to-menuentry.patch

BuildRequires: git
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: which
BuildRequires: gtk-doc
BuildRequires: glib-devel
BuildRequires: gobject-introspection
BuildRequires: gobject-introspection-devel
BuildRequires: gobject-introspection-python
BuildRequires: xz-devel
BuildRequires: icu-devel
BuildRequires: sqlite-devel
BuildRequires: mkinitcpio
BuildRequires: e2fsprogs-devel
BuildRequires: libpsl-devel
BuildRequires: zlib-devel
BuildRequires: curl-devel
BuildRequires: openssl-devel
BuildRequires: libsoup-devel
BuildRequires: attr-devel
BuildRequires: libarchive-devel
BuildRequires: fuse-devel
BuildRequires: libcap-devel
BuildRequires: gpgme-devel
BuildRequires: systemd-devel
BuildRequires: dracut
BuildRequires: bison

Requires: dracut
Requires: systemd
Requires: libassuan
Requires: gpgme

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
Requires: %{name}-libs = %{version}-%{release}

%description devel
The %{name}-devel package includes the header files for the %{name} library.

%package grub2
Summary: GRUB2 integration for OSTree
Group: Development/Libraries
Requires: grub2
Requires: grub2-efi
Requires: %{name} = %{version}-%{release}

%description grub2
GRUB2 integration for OSTree

%prep
%autosetup -p1

%build
env NOCONFIGURE=1 ./autogen.sh
%configure \
     --disable-silent-rules \
     --enable-gtk-doc \
     --with-dracut \
     --with-mkinitcpio \
     --without-selinux \
     --enable-libsoup-client-certs

%make_build

%install
%make_install %{?_smp_mflags}
install -D -m 0644 %{SOURCE1} %{buildroot}%{_presetdir}/91-%{name}.preset
install -vdm 755 %{buildroot}%{_sysconfdir}/%{name}/remotes.d

%post
%systemd_post %{name}-remount.service

%preun
%systemd_preun %{name}-remount.service

%postun
%systemd_postun_with_restart %{name}-remount.service

%files
%defattr(-,root,root)
%doc COPYING
%doc README.md
%{_bindir}/%{name}
%{_bindir}/rofiles-fuse
%{_datadir}/%{name}
%{_libdir}/initcpio/*
%dir %{_libdir}/dracut/modules.d/98ostree
%{_unitdir}/%{name}*.service
%{_unitdir}/%{name}-finalize-staged.path
%{_libdir}/dracut/modules.d/98ostree/*
%{_mandir}/man1/%{name}-admin*
%{_systemdgeneratordir}/%{name}-system-generator
%{_presetdir}/91-%{name}.preset
%exclude %{_sysconfdir}/grub.d/*%{name}
%exclude %{_libexecdir}/libostree/grub2*
%{_libdir}/%{name}/%{name}-prepare-root
%{_sysconfdir}/dracut.conf.d/%{name}.conf
%{_sysconfdir}/%{name}-mkinitcpio.conf
%{_libdir}/%{name}/%{name}-remount
%{_tmpfilesdir}/%{name}-tmpfiles.conf
%{_libexecdir}/libostree/*

%files libs
%defattr(-,root,root)
%{_sysconfdir}/%{name}
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/OSTree-1.0.typelib

%files devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_prefix}/share/bash-completion/completions/%{name}
%{_datadir}/gtk-doc/html/%{name}
%{_datadir}/gir-1.0/OSTree-1.0.gir
%exclude %{_mandir}/man1/%{name}-admin*
%{_mandir}/man1/*.gz
%{_mandir}/man5/*.gz

%files grub2
%defattr(-,root,root)
%{_sysconfdir}/grub.d/*%{name}
%{_libexecdir}/libostree/grub2*

%changelog
* Mon Jul 31 2023 Shreenidhi Shedi <sshedi@vmware.com> 2019.2-5
- Spec cleanups & fix requires
* Fri Oct 16 2020 Ashwin H <ashwinh@vmware.com> 2019.2-4
- Bump up to use new icu lib.
* Thu Oct 24 2019 Ankit Jain <ankitja@vmware.com> 2019.2-3
- Added for ARM Build
* Fri Sep 13 2019 Ankit Jain <ankitja@vmware.com> 2019.2-2
- Added support to get kernel and systemd commandline param
- from photon.cfg and systemd.cfg
* Tue May 14 2019 Ankit Jain <ankitja@vmware.com> 2019.2-1
- Initial build. First version
