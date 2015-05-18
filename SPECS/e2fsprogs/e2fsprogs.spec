Summary:	Contains the utilities for the ext2 file system
Name:		e2fsprogs
Version:	1.42.9
Release:	1
License:	GPLv2+
URL:		http://e2fsprogs.sourceforge.net
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://prdownloads.sourceforge.net/e2fsprogs/%{name}-%{version}.tar.gz
%description
The E2fsprogs package contains the utilities for handling
the ext2 file system.
%package	devel
Summary:	Header and development files for e2fsprogs
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create applications 
%prep
%setup -q
install -vdm 755 build
sed -i -e 's|^LD_LIBRARY_PATH.*|&:/tools/lib|' tests/test_config
%build
cd build
LIBS=-L/tools/lib \
CFLAGS=-I/tools/include \
PKG_CONFIG_PATH=/tools/lib/pkgconfig \
../configure \
	--prefix=%{_prefix} \
	--with-root-prefix='' \
	--enable-elf-shlibs \
	--disable-libblkid \
	--disable-libuuid \
	--disable-uuidd \
	--disable-fsck \
	--disable-silent-rules
make %{?_smp_mflags}
%install
cd build
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install-libs
chmod -v u+w %{buildroot}/%{_libdir}/{libcom_err,libe2p,libext2fs,libss}.a
rm -rf %{buildroot}%{_infodir}
%check
cd build
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
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
%{_mandir}/man3/*
%{_sbindir}/e4defrag
%{_sbindir}/filefrag
%{_sbindir}/e2freefrag
%{_sbindir}/mklost+found
/lib/libss.so.2
/lib/libext2fs.so.2.4
/lib/libcom_err.so.2.1
/lib/libss.so.2.0
/lib/libe2p.so.2.3
/lib/libcom_err.so.2
/lib/libe2p.so.2
/lib/libext2fs.so.2
/sbin/e2label
/sbin/e2image
/sbin/tune2fs
/sbin/e2undo
/sbin/debugfs
/sbin/e2fsck
/sbin/fsck.ext3
/sbin/mkfs.ext4
/sbin/dumpe2fs
/sbin/mke2fs
/sbin/fsck.ext4dev
/sbin/mkfs.ext2
/sbin/mkfs.ext4dev
/sbin/fsck.ext4
/sbin/badblocks
/sbin/logsave
/sbin/resize2fs
/sbin/fsck.ext2
/sbin/mkfs.ext3
%{_libdir}/libcom_err.so
%{_libdir}/libe2p.so
%{_libdir}/libext2fs.so
%lang(ca) %{_datarootdir}/locale/ca/LC_MESSAGES/e2fsprogs.mo
%lang(cs) %{_datarootdir}/locale/cs/LC_MESSAGES/e2fsprogs.mo
%lang(de) %{_datarootdir}/locale/de/LC_MESSAGES/e2fsprogs.mo
%lang(es) %{_datarootdir}/locale/es/LC_MESSAGES/e2fsprogs.mo
%lang(fr) %{_datarootdir}/locale/fr/LC_MESSAGES/e2fsprogs.mo
%lang(id) %{_datarootdir}/locale/id/LC_MESSAGES/e2fsprogs.mo
%lang(it) %{_datarootdir}/locale/it/LC_MESSAGES/e2fsprogs.mo
%lang(nl) %{_datarootdir}/locale/nl/LC_MESSAGES/e2fsprogs.mo
%lang(pl) %{_datarootdir}/locale/pl/LC_MESSAGES/e2fsprogs.mo
%lang(sv) %{_datarootdir}/locale/sv/LC_MESSAGES/e2fsprogs.mo
%lang(tr) %{_datarootdir}/locale/tr/LC_MESSAGES/e2fsprogs.mo
%lang(vi) %{_datarootdir}/locale/vi/LC_MESSAGES/e2fsprogs.mo
%lang(zh_CN) %{_datarootdir}/locale/zh_CN/LC_MESSAGES/e2fsprogs.mo

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
%{_includedir}/e2p/e2p.h
%{_includedir}/quota/mkquota.h
%{_includedir}/com_err.h
%{_libdir}/libcom_err.a
%{_libdir}/libss.a
%{_libdir}/pkgconfig/ss.pc
%{_libdir}/pkgconfig/ext2fs.pc
%{_libdir}/pkgconfig/quota.pc
%{_libdir}/pkgconfig/com_err.pc
%{_libdir}/pkgconfig/e2p.pc
%{_libdir}/libe2p.a
%{_libdir}/libquota.a
%{_libdir}/libext2fs.a
%{_libdir}/libss.so
%changelog
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.42.9-1
-	Initial build. First version

