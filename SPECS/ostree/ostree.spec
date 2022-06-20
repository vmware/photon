Summary:        Git for operating system binaries
Name:           ostree
Version:        2021.3
Release:        4%{?dist}
License:        LGPLv2+
URL:            https://ostree.readthedocs.io/en/latest
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

# Manually created Source tar which is equal to
# Source0 + .git as it requires git hooks at build time
Source0:        https://github.com/ostreedev/ostree/archive/%{name}-%{version}.tar.gz
%define sha512  %{name}-%{version}=a462ce6b8dde9c2984cee26c4828e9db4468d7311c61dddc1399a2c5b04602f777c65b40c79d00477db77d2b142f85c41119d1f8bac1f57a66ee326c7d2d2d97
Source1:        91-ostree.preset

Patch0:         dualboot-support.patch
Patch1:         0001-ostree-Copying-photon-config-to-boot-directory.patch
Patch2:         0002-ostree-Adding-load-env-to-menuentry.patch

BuildRequires:  git
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  which
BuildRequires:  gtk-doc
BuildRequires:  glib-devel
BuildRequires:  gobject-introspection
BuildRequires:  gobject-introspection-devel
BuildRequires:  xz-devel
BuildRequires:  sqlite-devel
BuildRequires:  mkinitcpio
BuildRequires:  e2fsprogs-devel
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
Requires: libsoup

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
%autosetup -p1

%build
env NOCONFIGURE=1 ./autogen.sh
%configure \
     --disable-silent-rules \
     --enable-gtk-doc \
     --with-dracut \
     --with-mkinitcpio \
     --with-selinux \
     --enable-libsoup-client-certs

%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete
install -D -m 0644 %{SOURCE1} %{buildroot}%{_presetdir}/91-ostree.preset
install -vdm 755 %{buildroot}%{_sysconfdir}/%{name}/remotes.d

%post
%systemd_post ostree-remount.service

%preun
%systemd_preun ostree-remount.service

%postun
%systemd_postun_with_restart ostree-remount.service

%files
%defattr(-,root,root)
%doc COPYING
%doc README.md
%{_bindir}/%{name}
%{_bindir}/rofiles-fuse
%{_datadir}/%{name}
%{_libdir}/initcpio/*
%dir %{_libdir}/dracut/modules.d/98ostree
%{_unitdir}/%{name}-finalize-staged.path
%{_libdir}/dracut/modules.d/98ostree/*
%{_systemdgeneratordir}/%{name}-system-generator
%{_presetdir}/91-ostree.preset
%{_unitdir}/%{name}*.service
%{_libdir}/%{name}/%{name}-prepare-root
%{_libdir}/%{name}/%{name}-remount
%{_tmpfilesdir}/%{name}-tmpfiles.conf
%config(noreplace) %{_sysconfdir}/dracut.conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}-mkinitcpio.conf
%{_mandir}/man1/%{name}-admin*
%{_libexecdir}/libostree/*
%exclude %{_sysconfdir}/grub.d/*ostree
%exclude %{_libexecdir}/libostree/grub2*

%files libs
%defattr(-,root,root)
%{_sysconfdir}/%{name}
%{_libdir}/*.so.1*
%{_libdir}/girepository-1.0/OSTree-1.0.typelib

%files devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/gtk-doc/html/%{name}
%{_datadir}/gir-1.0/OSTree-1.0.gir
%exclude %{_mandir}/man1/%{name}-admin*
%{_mandir}/man1/*.gz
%{_mandir}/man5/*.gz

%files grub2
%defattr(-,root,root)
%{_sysconfdir}/grub.d/*ostree
%{_libexecdir}/libostree/grub2*

%changelog
* Tue Jun 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 2021.3-4
- Bump version as a part of sqlite upgrade
* Tue Dec 07 2021 Alexey Makhalov <amakhalov@vmware.com> 2021.3-3
- Do not depend on icu and libpsl and libsoup will bring them
* Thu Sep 02 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2021.3-2
- Bump up for openssl
* Sat Aug 28 2021 Ankit Jain <ankitja@vmware.com> 2021.3-1
- Updated to 2021.3
* Thu Sep 03 2020 Ankit Jain <ankitja@vmware.com> 2020.6-1
- Updated to 2020.6
* Thu Aug 13 2020 Ankit Jain <ankitja@vmware.com> 2020.4-1
- Updated to 2020.4
* Mon Jun 22 2020 Tapas Kundu <tkundu@vmware.com> 2019.2-4
- Build with gobject-introspection-python3
* Thu Oct 24 2019 Ankit Jain <ankitja@vmware.com> 2019.2-3
- Added for ARM Build
* Fri Sep 13 2019 Ankit Jain <ankitja@vmware.com> 2019.2-2
- Added support to get kernel and systemd commandline param
- from photon.cfg and systemd.cfg
* Tue May 14 2019 Ankit Jain <ankitja@vmware.com> 2019.2-1
- Initial build. First version
