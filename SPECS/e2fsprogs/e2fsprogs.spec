Summary:        Contains the utilities for the ext2 file system
Name:           e2fsprogs
Version:        1.44.3
Release:        2%{?dist}
License:        GPLv2+
URL:            http://e2fsprogs.sourceforge.net
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://prdownloads.sourceforge.net/e2fsprogs/%{name}-%{version}.tar.gz
%define sha1    e2fsprogs=bfe11b75fee61c4d3795ac27eea11f9f7843294b
Requires:       %{name}-libs = %{version}-%{release}
Conflicts:      toybox

%description
The E2fsprogs package contains the utilities for handling the ext2 file system.

%package    libs
Summary:    contains libraries used by other packages
%description    libs
It contains the libraries: libss and libcom_err

%package    devel
Summary:    Header and development files for e2fsprogs
Requires:   %{name} = %{version}
%description    devel
It contains the libraries and header files to create applications

%package lang
Summary: Additional language files for e2fsprogs
Group:   System Environment/Base
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of e2fsprogs

%prep
%setup -q
sed -i -e 's|^LD_LIBRARY_PATH.*|&:/tools/lib|' tests/test_config

%build
LIBS=-L/tools/lib \
CFLAGS=-I/tools/include \
PKG_CONFIG_PATH=/tools/lib/pkgconfig \
%configure \
    --with-root-prefix='' \
    --enable-elf-shlibs \
    --disable-libblkid \
    --disable-libuuid \
    --disable-uuidd \
    --disable-fsck \
    --disable-silent-rules \
    --enable-symlink-install
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install-libs
chmod -v u+w %{buildroot}/%{_libdir}/{libcom_err,libe2p,libext2fs,libss}.a
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%config %{_sysconfdir}/mke2fs.conf
%{_bindir}/compile_et
%{_bindir}/mk_cmds
%{_bindir}/chattr
%{_bindir}/lsattr
%{_libdir}/e2initrd_helper
%{_datadir}/ss/ct_c.awk
%{_datadir}/ss/ct_c.sed
%{_datadir}/et/et_h.awk
%{_datadir}/et/et_c.awk
%{_mandir}/man8/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_sbindir}/*
%{_libdir}/libext2fs.so.2.4
%{_libdir}/libe2p.so.2.3
%{_libdir}/libe2p.so.2
%{_libdir}/libext2fs.so.2
%{_libdir}/libe2p.so
%{_libdir}/libext2fs.so

%files libs
%{_libdir}/libss.so
%{_libdir}/libss.so.*
%{_libdir}/libcom_err.*

%files devel
%{_includedir}/ss/ss_err.h
%{_includedir}/ss/ss.h
%{_includedir}/et/com_err.h
%{_includedir}/ext2fs/ext2_io.h
%{_includedir}/ext2fs/ext2_fs.h
%{_includedir}/ext2fs/tdb.h
%{_includedir}/ext2fs/qcow2.h
%{_includedir}/ext2fs/bitops.h
%{_includedir}/ext2fs/ext2_err.h
%{_includedir}/ext2fs/ext2fs.h
%{_includedir}/ext2fs/ext3_extents.h
%{_includedir}/ext2fs/ext2_types.h
%{_includedir}/ext2fs/ext2_ext_attr.h
%{_includedir}/ext2fs/hashmap.h
%{_includedir}/e2p/e2p.h
%{_includedir}/com_err.h
%{_libdir}/libcom_err.a
%{_libdir}/libss.a
%{_libdir}/pkgconfig/ss.pc
%{_libdir}/pkgconfig/ext2fs.pc
%{_libdir}/pkgconfig/com_err.pc
%{_libdir}/pkgconfig/e2p.pc
%{_libdir}/libe2p.a
%{_libdir}/libext2fs.a
%{_mandir}/man3/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*   Tue Oct 2 2018 Michelle Wang <michellew@vmware.com> 1.44.3-2
-   Add conflicts toybox.
*   Mon Sep 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.44.3-1
-   Version update to fix compilation issue againts glibc-2.28.
*   Tue May 02 2017 Anish Swaminathan <anishs@vmware.com> 1.43.4-2
-   Add lang package.
*   Mon Apr 03 2017 Chang Lee <changlee@vmware.com> 1.43.4-1
-   Updated to version 1.43.4.
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.42.13-5
-   Moved man3 to devel subpackage.
*   Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 1.42.13-4
-   Create libs subpackage for krb5.
*   Tue Sep 20 2016 Alexey Makhalov <amakhalov@vmware.com> 1.42.13-3
-   Use symlinks - save a diskspace.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.42.13-2
-   GA - Bump release of all rpms.
*   Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 1.42.13-1
-   Updated to version 1.42.13.
*   Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 1.42.9-4
-   Edit post script.
*   Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 1.42.9-3
-   Handled locale files with macro find_lang.
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.42.9-2
-   Update according to UsrMove.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.42.9-1
-   Initial build First version.
