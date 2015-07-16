Summary:	Programs for compressing and decompressing files
Name:		xz
Version:	5.0.5
Release:	2%{?dist}
URL:		http://tukaani.org/xz
License:	GPLv2+ and GPLv3+ and LGPLv2+
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://tukaani.org/xz/%{name}-%{version}.tar.xz
%define sha1 xz=56f1d78117f0c32bbb1cfd40117aa7f55bee8765
%description
The Xz package contains programs for compressing and
decompressing files
%package	devel
Summary:	Header and development files for xz
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create applications 
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--docdir=%{_defaultdocdir}/%{name}-%{version} \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} pkgconfigdir=%{_libdir}/pkgconfig install
install -vdm 755 %{buildroot}/{bin,%_lib}
mv -v   %{buildroot}%{_bindir}/{lzma,unlzma,lzcat,xz,unxz,xzcat} %{buildroot}/bin
ln -svf "../..%{_lib}/$(readlink %{buildroot}%{_libdir}/liblzma.so)" %{buildroot}%{_libdir}/liblzma.so
find %{buildroot}%{_libdir} -name '*.la' -delete
%find_lang %{name}
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files -f %{name}.lang
%defattr(-,root,root)
/bin/xz
/bin/lzcat
/bin/lzma
/bin/xzcat
/bin/unlzma
/bin/unxz
%{_bindir}/xzless
%{_bindir}/lzmadec
%{_bindir}/xzcmp
%{_bindir}/lzegrep
%{_bindir}/lzcmp
%{_bindir}/xzfgrep
%{_bindir}/xzmore
%{_bindir}/lzgrep
%{_bindir}/xzdiff
%{_bindir}/lzfgrep
%{_bindir}/xzegrep
%{_bindir}/lzless
%{_bindir}/lzdiff
%{_bindir}/lzmore
%{_bindir}/lzmainfo
%{_bindir}/xzgrep
%{_bindir}/xzdec
%{_libdir}/liblzma.so.5.0.5
%{_libdir}/liblzma.so.5
%{_mandir}/man1/*
%{_defaultdocdir}/%{name}-%{version}/*
%files devel
%{_includedir}/lzma.h
%{_includedir}/lzma/index_hash.h
%{_includedir}/lzma/index.h
%{_includedir}/lzma/stream_flags.h
%{_includedir}/lzma/vli.h
%{_includedir}/lzma/version.h
%{_includedir}/lzma/check.h
%{_includedir}/lzma/lzma.h
%{_includedir}/lzma/hardware.h
%{_includedir}/lzma/block.h
%{_includedir}/lzma/filter.h
%{_includedir}/lzma/container.h
%{_includedir}/lzma/bcj.h
%{_includedir}/lzma/base.h
%{_includedir}/lzma/delta.h
%{_libdir}/pkgconfig/liblzma.pc
%{_libdir}/liblzma.a
%{_libdir}/liblzma.so
%changelog
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 5.0.5-2
-   Update according to UsrMove.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.0.5-1
-	Initial build.	First version
