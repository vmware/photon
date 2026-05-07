%global build_if %{photon_subrelease} >= 91

Summary:        Utilities for creating and managing EROFS filesystems
Name:           erofs-utils
Version:        1.9.1
Release:        1%{?dist}
URL:            https://github.com/erofs/erofs-utils
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/erofs/erofs-utils/archive/refs/tags/%{name}-%{version}.tar.gz

Source1:        license.txt
%include        %{SOURCE1}

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkg-config
BuildRequires:  lz4-devel
BuildRequires:  xz-devel
BuildRequires:  zstd-devel
BuildRequires:  zlib-devel
BuildRequires:  util-linux-devel
BuildRequires:  fuse-devel

Requires:       lz4
Requires:       xz-libs
Requires:       zstd-libs
Requires:       zlib
Requires:       util-linux-libs

%description
The erofs-utils package contains utilities for creating and managing EROFS
(Enhanced Read-Only File System) filesystems. EROFS is a lightweight
read-only file system with modern designs for scenarios which need
high-performance read-only requirements.

%package        fuse
Summary:        FUSE support for EROFS filesystems
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}
Requires:       fuse

%description    fuse
This package provides erofsfuse, a FUSE-based utility for mounting
EROFS filesystems in userspace.

%package        doc
Summary:        Documentation and man pages for EROFS utilities
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}

%description    doc
This package provides documentation and man pages for erofs-utils.

%prep
%autosetup -p1

%build
./autogen.sh
%configure \
    --enable-lz4 \
    --enable-lzma \
    --enable-fuse \
    --with-libzstd

%make_build

%install
%make_install

%files
%defattr(-,root,root)
%{_bindir}/mkfs.erofs
%{_bindir}/dump.erofs
%{_bindir}/fsck.erofs
%{_sbindir}/mount.erofs

%files fuse
%defattr(-,root,root)
%{_bindir}/erofsfuse

%files doc
%defattr(-,root,root)
%{_mandir}/man1/mkfs.erofs.1*
%{_mandir}/man1/dump.erofs.1*
%{_mandir}/man1/fsck.erofs.1*
%{_mandir}/man8/mount.erofs.8*
%{_mandir}/man1/erofsfuse.1*

%changelog
* Wed Apr 15 2026 Oliver Kurth <oliver.kurth@broadcom.com> 1.9.1-1
- Initial build of erofs-utils
