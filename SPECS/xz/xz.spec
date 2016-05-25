Summary:	Programs for compressing and decompressing files
Name:		xz
Version:	5.2.2
Release:	2%{?dist}
URL:		http://tukaani.org/xz
License:	GPLv2+ and GPLv3+ and LGPLv2+
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://tukaani.org/xz/%{name}-%{version}.tar.xz
%define sha1 xz=72c567d3263345844191a7e618779b179d1f49e0
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
%{_libdir}/liblzma.so.5.2.2
%{_libdir}/liblzma.so.5
%{_mandir}/man1/*
%{_defaultdocdir}/%{name}-%{version}/*
%files devel
%{_includedir}/lzma.h
%{_includedir}/lzma/*.h
%{_libdir}/pkgconfig/liblzma.pc
%{_libdir}/liblzma.a
%{_libdir}/liblzma.so
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 	5.2.2-2
-	GA - Bump release of all rpms
*   Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 5.2.2-1
-   Upgrade version.
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 5.0.5-2
-   Update according to UsrMove.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.0.5-1
-   Initial build.	First version
